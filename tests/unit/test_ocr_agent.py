from agents.models import UserRequest
from agents.ocr_agent import OCRAgent


def test_ocr_agent_requires_image():
    agent = OCRAgent()

    result = agent.analyze(
        UserRequest(prompt="Read this label.")
    )

    assert result.visible_text == ""
    assert "No image" in result.summary
    assert result.uncertainty is not None


def test_ocr_agent_reads_label_stub():
    agent = OCRAgent()

    result = agent.analyze(
        UserRequest(
            prompt="Read this medicine label.",
            image_path="medicine-label.jpg",
        )
    )

    assert "Take one tablet" in result.visible_text
    assert "one tablet" in result.important_values


def test_ocr_agent_reads_receipt_stub():
    agent = OCRAgent()

    result = agent.analyze(
        UserRequest(
            prompt="Read this receipt.",
            image_path="receipt.jpg",
        )
    )

    assert "$12.50" in result.visible_text
    assert "$12.50" in result.important_values


def test_ocr_agent_handles_no_text_stub():
    agent = OCRAgent()

    result = agent.analyze(
        UserRequest(
            prompt="Describe this image.",
            image_path="scene.jpg",
        )
    )

    assert result.visible_text == ""
    assert "No readable text" in result.summary


def test_ocr_agent_handles_gemini_exception_gracefully(monkeypatch):
    from agents.gemini_vision_client import GeminiVisionClient
    monkeypatch.setattr(GeminiVisionClient, "is_available", lambda self: True)

    def mock_analyze_image(self, image_path, prompt):
        raise RuntimeError("API error 503 Service Unavailable")
    monkeypatch.setattr(GeminiVisionClient, "analyze_image", mock_analyze_image)

    agent = OCRAgent()
    result = agent.analyze(
        UserRequest(
            prompt="Read this medicine label.",
            image_path="medicine-label.jpg",
        )
    )

    assert "Take one tablet" in result.visible_text
    assert result.uncertainty == (
        "Gemini is temporarily unavailable, so I used the safe local fallback. "
        "Please try again later for live text reading."
    )