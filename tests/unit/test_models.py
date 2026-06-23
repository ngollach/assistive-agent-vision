from agents.models import (
    AgentResult,
    FinalResponse,
    OCRFinding,
    RequiredAction,
    RiskLevel,
    SafetyFinding,
    UserRequest,
    VisionFinding,
)


def test_agent_models_can_be_created():
    request = UserRequest(
        prompt="What is in front of me?",
        image_path="sample.jpg",
    )

    vision = VisionFinding(
        summary="A desk with a laptop and a bottle.",
        objects=["laptop", "bottle"],
        spatial_details=["Bottle is near the front-right edge."],
        possible_hazards=["Bottle may be close to the edge."],
        uncertainty=None,
    )

    ocr = OCRFinding(
        visible_text="",
        summary="No visible text detected.",
        important_values=[],
        uncertainty=None,
    )

    safety = SafetyFinding(
        risk_level=RiskLevel.MEDIUM,
        reason="The response involves physical object location.",
        required_action=RequiredAction.CAUTION,
        caution_message="Be careful reaching forward.",
    )

    result = AgentResult(
        user_request=request,
        vision=vision,
        ocr=ocr,
        safety=safety,
    )

    final = FinalResponse(
        answer="I see a desk with a laptop and a bottle. Be careful reaching forward.",
        risk_level=result.safety.risk_level,
    )

    assert final.risk_level == RiskLevel.MEDIUM
    assert "desk" in final.answer
    assert result.vision.objects == ["laptop", "bottle"]