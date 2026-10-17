
import requests

# Ollama's local API address
OLLAMA_URL = "http://localhost:11434/api/generate"

# Send a test prompt to our local model
payload = {
    "model": "qwen2.5:3b",
    "prompt": (
        "You are a sales research assistant. "
        "In two sentences, explain why a sales representative "
        "should research a prospective company before a meeting."
    ),
    "stream": False,
}

# Send the request and get the model's response
response = requests.post(OLLAMA_URL, json=payload, timeout=180)
response.raise_for_status()

# Print the generated answer
result = response.json()
print(result["response"])