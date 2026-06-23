from agents.gemini_vision_client import GeminiVisionClient


def test_gemini_vision_client_unavailable_without_api_key(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    client = GeminiVisionClient()

    assert client.is_available() is False