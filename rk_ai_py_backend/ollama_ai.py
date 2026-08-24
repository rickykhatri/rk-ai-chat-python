# import os
# import json
# import requests

# from dotenv import load_dotenv
# from fastapi.responses import StreamingResponse


# load_dotenv(".env")

# ollama_model = os.getenv("ollama_model")
# ollama_base_url = os.getenv("ollama_base_url")


# def stream_ollama_response(prompt: str):

#     response = requests.post(
#         f"{ollama_base_url}/api/chat",
#          headers={
#             "Content-Type": "application/json",
#             "Accept": "application/x-ndjson"
#             #"ngrok-skip-browser-warning": "true"
#         },
#         json={
#             "model": ollama_model,
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             "stream": True
#         },
#         stream=True,
#         timeout=300
#     )

#     response.raise_for_status()

#     for line in response.iter_lines():

#         if not line:
#             continue

#         data = json.loads(line)

#         content = (
#             data
#             .get("message", {})
#             .get("content", "")
#         )

#         if content:
#             yield content


# def chat_with_ollama(prompt: str):

#     return StreamingResponse(
#         stream_ollama_response(prompt),
#         media_type="text/plain"
#     )

import os
import json
import requests

from dotenv import load_dotenv
from fastapi.responses import StreamingResponse

load_dotenv(".env")

ollama_model = os.getenv("ollama_model", "llama3.2")
ollama_base_url = os.getenv(
    "ollama_base_url",
    "http://localhost:11434"
).rstrip("/")


# Reuse HTTP connection
session = requests.Session()


def stream_ollama_response(prompt: str):
    url = f"{ollama_base_url}/api/chat"

    payload = {
    "model": ollama_model,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "stream": True,
    "options": {
        "num_ctx": 4096
    }
    }

    try:
        with session.post(
            url,
            json=payload,
            stream=True,
            timeout=(10, 600)
        ) as response:

            response.raise_for_status()

            for line in response.iter_lines(
                chunk_size=1,
                decode_unicode=True
            ):
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                content = (
                    data
                    .get("message", {})
                    .get("content", "")
                )

                if content:
                    yield content

                if data.get("done"):
                    break

    except requests.RequestException as e:
        yield f"\n[Ollama error: {str(e)}]"


def chat_with_ollama(prompt: str):

    return StreamingResponse(
        stream_ollama_response(prompt),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )