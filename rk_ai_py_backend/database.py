from pymongo import MongoClient
from dotenv import load_dotenv  
import os
# Load environment variables from .env file
load_dotenv(dotenv_path=".env")  # Specify the path to your .env file

data_base_collection_name = os.getenv("collection_name")  # Get the collection name from environment variables  

 # Methdod to create a database connection
def create_database_connection():
    client = MongoClient(os.getenv("database_connection_uri"))
    db = client[os.getenv("database_name")]
    try:
        if db.client:
            print("Database connection successful")
        else:
            print("Database connection failed")
    except Exception as e:
        print(f"Database connection error: {e}")
    return db

# Method to insert a chat message into the database
def insert_chat_message(db, chat_message):
    chat_collection = db[data_base_collection_name]
    result = chat_collection.insert_one(chat_message)
    return result.inserted_id

# Method to retrieve all chat messages from the database
def get_all_chat_messages(db):
    chat_collection = db[data_base_collection_name]
    documents = chat_collection.find()
    for doc in documents:
        doc.pop('_id', None)  # Remove the '_id' field from each document
    return list(documents)
