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