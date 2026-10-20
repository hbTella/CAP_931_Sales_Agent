
def test_sales_agent_uses_local_ollama():
    """Confirm the project is configured to use the local model."""

    from cap_931_sales_agent import llm_client

    assert llm_client.MODEL_NAME == "qwen2.5:3b"
    assert llm_client.OLLAMA_URL == (
        "http://localhost:11434/api/generate"
    )
