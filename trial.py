from pymongo import MongoClient

uri = "mongodb+srv://kkaushik0203:stevejobs@authorization.hh4tmo0.mongodb.net/?retryWrites=true&w=majority&appName=authorization"
client = MongoClient(uri)

try:
    info = client.server_info()  # Raises an exception if auth fails
    print("Connected to MongoDB Atlas!")
except Exception as e:
    print("Error connecting to MongoDB Atlas:", e)