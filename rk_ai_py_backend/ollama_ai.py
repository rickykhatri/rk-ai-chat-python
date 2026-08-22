import os
import json
import requests

from dotenv import load_dotenv
from fastapi.responses import StreamingResponse


load_dotenv(".env")

ollama_model = os.getenv("ollama_model")
ollama_base_url = os.getenv("ollama_base_url")


def stream_ollama_response(prompt: str):

    response = requests.post(
        f"{ollama_base_url}/api/chat",
         headers={
            "Content-Type": "application/json",
            "Accept": "application/x-ndjson"
            #"ngrok-skip-browser-warning": "true"
        },
        json={
            "model": ollama_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": True
        },
        stream=True,
        timeout=300
    )

    response.raise_for_status()

    for line in response.iter_lines():

        if not line:
            continue

        data = json.loads(line)

        content = (
            data
            .get("message", {})
            .get("content", "")
        )

        if content:
            yield content


def chat_with_ollama(prompt: str):

    return StreamingResponse(
        stream_ollama_response(prompt),
        media_type="text/plain"
    )