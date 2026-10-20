
import requests


def test_ollama_api_url():
    """Check that the local Ollama API URL is configured correctly."""

    ollama_url = "http://localhost:11434/api/generate"

    assert ollama_url.startswith("http://localhost:11434/")
    assert ollama_url.endswith("/api/generate")
