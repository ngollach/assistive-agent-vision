from agents.models import UserRequest
from agents.vision_agent import VisionAgent


def test_vision_agent_requires_image():
    agent = VisionAgent()

    result = agent.analyze(
        UserRequest(prompt="Describe this image.")
    )

    assert result.summary == "No image was provided."
    assert result.uncertainty is not None


def test_vision_agent_returns_desk_stub_response():
    agent = VisionAgent()

    result = agent.analyze(
        UserRequest(
            prompt="What is on this desk?",
            image_path="sample-desk.jpg",
        )
    )

    assert "desk" in result.summary.lower() or "table" in result.summary.lower()
    assert result.uncertainty is not None


def test_vision_agent_returns_phone_stub_response():
    agent = VisionAgent()

    result = agent.analyze(
        UserRequest(
            prompt="Where is my phone?",
            image_path="sample-phone.jpg",
        )
    )

    assert "phone" in result.summary.lower()
    assert "phone" in result.objects


def test_vision_agent_handles_gemini_exception_gracefully(monkeypatch):
    from agents.gemini_vision_client import GeminiVisionClient
    monkeypatch.setattr(GeminiVisionClient, "is_available", lambda self: True)

    def mock_analyze_image(self, image_path, prompt):
        raise RuntimeError("API error 503 Service Unavailable")
    monkeypatch.setattr(GeminiVisionClient, "analyze_image", mock_analyze_image)

    agent = VisionAgent()
    result = agent.analyze(
        UserRequest(
            prompt="What is on this desk?",
            image_path="sample-desk.jpg",
        )
    )

    assert "desk" in result.summary.lower() or "table" in result.summary.lower()
    assert result.uncertainty == (
        "Gemini is temporarily unavailable, so I used the safe local fallback. "
        "Please try again later for live image analysis."
    )