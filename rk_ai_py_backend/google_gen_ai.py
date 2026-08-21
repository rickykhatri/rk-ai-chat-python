from fastapi import types
from google import genai
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv(dotenv_path=".env")  # Specify the path to your .env file
google_gen_ai_model = os.getenv("google_gen_ai_model")  # Get the Google Gen AI model from environment variables
google_gen_ai_api_key = os.getenv("google_gen_ai_api_key")  # Get the Google Gen AI API key from environment variables  

# Method to chat with Google Gen AI and return the response
def chat_with_google_gen_ai(prompt:str):
    client = genai.Client(api_key=google_gen_ai_api_key)
    response = client.models.generate_content(
        model=google_gen_ai_model,
        contents=prompt,
        config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
    candidates = getattr(response, "candidates", []) or []
    if not candidates:
        return ""

    content = getattr(candidates[0], "content", None)
    parts = getattr(content, "parts", []) or []
    if not parts:
        return ""

    return getattr(parts[0], "text", "")