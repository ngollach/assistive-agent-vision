from agents.models import (
    AgentResult,
    OCRFinding,
    RequiredAction,
    RiskLevel,
    SafetyFinding,
    UserRequest,
    VisionFinding,
)
from agents.response_agent import ResponseAgent


def test_response_agent_creates_scene_response():
    agent = ResponseAgent()

    result = AgentResult(
        user_request=UserRequest(prompt="What is in front of me?"),
        vision=VisionFinding(
            summary="I see a desk with a laptop and a bottle.",
            objects=["desk", "laptop", "bottle"],
            spatial_details=["The bottle is near the front-right edge."],
            possible_hazards=["The bottle may be easy to knock over."],
        ),
        safety=SafetyFinding(
            risk_level=RiskLevel.MEDIUM,
            reason="Object location may involve physical safety.",
            required_action=RequiredAction.CAUTION,
            caution_message="Use caution when reaching forward.",
        ),
    )

    response = agent.create_response(result)

    assert response.risk_level == RiskLevel.MEDIUM
    assert "desk" in response.answer
    assert "Use caution" in response.answer


def test_response_agent_reads_visible_text():
    agent = ResponseAgent()

    result = AgentResult(
        user_request=UserRequest(prompt="Read this label."),
        ocr=OCRFinding(
            visible_text="Take one tablet daily after food.",
            summary="The label appears to provide dosage instructions.",
        ),
        safety=SafetyFinding(
            risk_level=RiskLevel.LOW,
            reason="Reading visible text only.",
            required_action=RequiredAction.ALLOW,
        ),
    )

    response = agent.create_response(result)

    assert response.risk_level == RiskLevel.LOW
    assert "Visible text" in response.answer
    assert "Take one tablet" in response.answer


def test_response_agent_refuses_high_risk_medical_decision_but_reads_text():
    agent = ResponseAgent()

    result = AgentResult(
        user_request=UserRequest(prompt="Should I take this medicine?"),
        ocr=OCRFinding(
            visible_text="Take one tablet daily after food.",
            summary="The label appears to provide dosage instructions.",
        ),
        safety=SafetyFinding(
            risk_level=RiskLevel.HIGH,
            reason="The user asked for a medical decision.",
            required_action=RequiredAction.REFUSE,
            caution_message=(
                "I can help read visible text, but I cannot decide what medicine "
                "you should take. Please confirm with a doctor or pharmacist."
            ),
        ),
    )

    response = agent.create_response(result)

    assert response.risk_level == RiskLevel.HIGH
    assert "Visible text" in response.answer
    assert "cannot decide" in response.answer
    assert "doctor or pharmacist" in response.answer


def test_response_agent_includes_uncertainty():
    agent = ResponseAgent()

    result = AgentResult(
        user_request=UserRequest(prompt="Describe this blurry image."),
        vision=VisionFinding(
            summary="I can make out a table-like surface.",
            uncertainty="The image is blurry, so details may be incomplete.",
        ),
        safety=SafetyFinding(
            risk_level=RiskLevel.LOW,
            reason="No high-risk category detected.",
            required_action=RequiredAction.ALLOW,
        ),
    )

    response = agent.create_response(result)

    assert response.uncertainty is not None
    assert "blurry" in response.answer

def test_response_agent_includes_task_guidance():
    agent = ResponseAgent()

    result = AgentResult(
        user_request=UserRequest(prompt="Where is my phone?"),
        task_guidance=[
            "Move slowly and carefully.",
            "Confirm with touch or another trusted method before acting.",
        ],
        safety=SafetyFinding(
            risk_level=RiskLevel.LOW,
            reason="No high-risk category detected.",
            required_action=RequiredAction.ALLOW,
        ),
    )

    response = agent.create_response(result)

    assert "Guidance:" in response.answer
    assert "Move slowly" in response.answer