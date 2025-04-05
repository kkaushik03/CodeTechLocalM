from flask import Flask, request, jsonify
import requests
import os
import threading

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'py'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def warmup_model():
    """
    Sends a small request to Ollama to warm up the model.
    This helps ensure the model is loaded into memory before processing real requests.
    """
    try:
        print("Warming up model...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": "Hello", "stream": False},
            timeout=180  # generous timeout for model loading
        )
        print("Warmup response:", response.text)
    except Exception as e:
        print("Warmup error:", e)

@app.route('/')
def home():
    return '🚀 Flask server is running! POST to /upload with a Python file.'

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the 'file' field is in the request.
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only .py files are allowed'}), 400

    print("Received file:", file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        with open(file_path, 'r') as f:
            file_content = f.read()

        # Truncate file content if it exceeds 8000 characters to avoid token or memory issues.
        if len(file_content) > 8000:
            file_content = file_content[:8000] + "\n# Truncated due to length"

        prompt = f"Grade this Python code and give helpful, constructive feedback:\n\n{file_content}"

        # Send the request to Ollama with an extended timeout.
        ollama_response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=180  # Adjust as necessary
        )

        if ollama_response.status_code != 200:
            return jsonify({
                'error': 'Ollama API error',
                'status_code': ollama_response.status_code,
                'response': ollama_response.text
            }), 500

        response_json = ollama_response.json()
        return jsonify({
            "response": response_json.get("response", "No response received."),
            "model_used": "mistral"
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Ollama API call failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    # Start the warmup in a background thread.
    threading.Thread(target=warmup_model).start()
    # Disable the reloader to avoid file changes in the uploads folder triggering restarts.
    app.run(debug=True, use_reloader=False)