from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import threading
import uuid
import json
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Use environment variables for configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# MongoDB connection setup using environment variables.
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)

# Test the connection to MongoDB Atlas.
try:
    info = client.server_info()  # Raises an exception if auth fails
    print("Connected to MongoDB Atlas!")
except Exception as e:
    print("Error connecting to MongoDB Atlas:", e)

# Choose the database and collection.
db_name = os.getenv('DB_NAME', 'credentials')
db = client[db_name]
users_collection = db['users']

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'py'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def warmup_model():
    try:
        print("Warming up model...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": "Hello", "stream": False},
            timeout=180
        )
        print("Warmup response:", response.text)
    except Exception as e:
        print("Warmup error:", e)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Registration endpoint: Store username and hashed password in MongoDB.
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    # Check if the user already exists in MongoDB.
    if users_collection.find_one({"username": username}):
        return jsonify({"msg": "User already exists"}), 400

    # Hash the password and store the user.
    hashed_password = generate_password_hash(password)
    user = {"username": username, "password": hashed_password}
    users_collection.insert_one(user)

    return jsonify({"msg": "User registered successfully."}), 201

# Login endpoint: Authenticate against MongoDB-stored credentials.
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# (Optional) The file upload and report generation endpoints remain unchanged.
@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only .py files are allowed'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        with open(file_path, 'r') as f:
            file_content = f.read()

        if len(file_content) > 8000:
            file_content = file_content[:8000] + "\n# Truncated due to length"

        prompt = f"Grade this Python code and give helpful, constructive feedback:\n\n{file_content}"

        ollama_response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=180
        )

        if ollama_response.status_code != 200:
            return jsonify({
                'error': 'Ollama API error',
                'status_code': ollama_response.status_code,
                'response': ollama_response.text
            }), 500

        response_json = ollama_response.json()
        report = response_json.get("response", "No response received.")
        unique_id = str(uuid.uuid4())
        result_data = {
            "id": unique_id,
            "file": {
                "filename": file.filename,
                "content": file_content
            },
            "report": report
        }
        result_file_path = os.path.join(RESULTS_FOLDER, f"{unique_id}.json")
        with open(result_file_path, "w") as result_file:
            json.dump(result_data, result_file)

        return jsonify(result_data)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Ollama API call failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    threading.Thread(target=warmup_model).start()
    app.run(debug=True, use_reloader=False)