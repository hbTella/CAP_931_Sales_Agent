
from cap_931_sales_agent import llm_client


def test_generate_response_returns_model_text(monkeypatch):
    """Check the LLM client without calling Ollama."""

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"response": "Research helps sales representatives prepare."}

    def fake_post(url, json, timeout):
        assert url == llm_client.OLLAMA_URL
        assert json["model"] == llm_client.MODEL_NAME
        assert json["prompt"] == "Explain why company research matters."
        assert json["stream"] is False
        return FakeResponse()

    monkeypatch.setattr(llm_client.requests, "post", fake_post)

    result = llm_client.generate_response(
        "Explain why company research matters."
    )

    assert result == "Research helps sales representatives prepare."
