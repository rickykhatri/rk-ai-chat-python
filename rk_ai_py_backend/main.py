
from click import prompt
from ollama_ai import chat_with_ollama
from fastapi import FastAPI
from database import create_database_connection, insert_chat_message, get_all_chat_messages
from fastapi.staticfiles import StaticFiles

import google_search

app = FastAPI()

@app.get("/")
def read_root():
    user = {
        "name": "Ricky",
        "age": 30
    }
    return {
        "message": "Welcome to the RK AI Chat API",
    }

@app.post("/chat/{message}") 
def post_chat(message:str):
    db = create_database_connection()
    chat_data = {
        "chat_message": message,
    }
    inserted_id = insert_chat_message(db, chat_data)
    return {"message": "Chat message inserted successfully", "inserted_id": str(inserted_id)}

# Method to retrieve chat history from the database
@app.get("/chats")
def get_chat_history():
    db = create_database_connection()
    chat_messages = get_all_chat_messages(db)
    return {"chat_history": chat_messages}

# Method to perform a Google search and return the HTML response
@app.get("/search/{query}")
def search_google(query: str):
    search_results = google_search.search_google(query)
    return {"search_results": search_results}

# Method to chat with Google Gen AI and return the response
# @app.post("/chat_ai/{prompt}")
# async def chat_with_google_gen_ai_endpoint(prompt: str):
#     # from google_gen_ai import chat_with_google_gen_ai
#     # ai_response = chat_with_google_gen_ai(prompt)
#     from ollama_ai import chat_with_ollama
#     ai_response = chat_with_ollama(prompt)
#     return {"response": ai_response}

# Method to chat with Ollama AI and return the response
@app.get("/chat_ai/{prompt}")
def chat_ai(prompt: str):
    return chat_with_ollama(prompt)

# --------------------------------------------------
# Serve frontend
# --------------------------------------------------

app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)