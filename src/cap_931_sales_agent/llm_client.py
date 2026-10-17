
import requests

# Local Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# Model used by the CAP 931 Sales Assistant
MODEL_NAME = "qwen2.5:3b"


def generate_response(prompt: str) -> str:
    """Send a prompt to the local model and return its response."""

    payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False,
    "options": {
        "num_predict": 400,
    },
}

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180,
    )
    response.raise_for_status()

    return response.json()["response"]