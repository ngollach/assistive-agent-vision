from agents.models import RequiredAction, RiskLevel, SafetyFinding
from agents.task_guidance_agent import TaskGuidanceAgent


def test_task_guidance_for_finding_object():
    agent = TaskGuidanceAgent()

    guidance = agent.create_guidance("Where is my phone?")

    assert "Move slowly" in guidance[0]
    assert any("trusted method" in item for item in guidance)


def test_task_guidance_for_reading_label():
    agent = TaskGuidanceAgent()

    guidance = agent.create_guidance("Read this medicine label.")

    assert any("visible text" in item for item in guidance)
    assert any("verify" in item for item in guidance)


def test_task_guidance_refuses_when_safety_refuses():
    agent = TaskGuidanceAgent()

    safety = SafetyFinding(
        risk_level=RiskLevel.HIGH,
        reason="Medical decision requested.",
        required_action=RequiredAction.REFUSE,
        caution_message="Please ask a doctor or pharmacist.",
    )

    guidance = agent.create_guidance(
        prompt="Should I take this medicine?",
        safety=safety,
    )

    assert "cannot safely" in guidance[0]


def test_task_guidance_for_medium_risk():
    agent = TaskGuidanceAgent()

    safety = SafetyFinding(
        risk_level=RiskLevel.MEDIUM,
        reason="Physical safety involved.",
        required_action=RequiredAction.CAUTION,
        caution_message="Use caution.",
    )

    guidance = agent.create_guidance(
        prompt="Can I move forward?",
        safety=safety,
    )

    assert any("safety guarantee" in item for item in guidance)

def test_task_guidance_returns_empty_for_clear_image_description():
    agent = TaskGuidanceAgent()

    # Clear image-description requests when an image is provided
    for prompt in ["Describe this image.", "What is in front of me?", "Describe this desk."]:
        guidance = agent.create_guidance(
            prompt=prompt,
            image_provided=True,
        )
        assert guidance == []


def test_task_guidance_asks_for_image_when_missing():
    agent = TaskGuidanceAgent()

    # Generic/clear image-description requests when an image is missing
    for prompt in ["Describe this image.", "What is in front of me?", "Describe this desk."]:
        guidance = agent.create_guidance(
            prompt=prompt,
            image_provided=False,
        )
        assert guidance == ["Please provide an image and a specific question."]


def test_task_guidance_retains_specific_guidance_even_if_image_is_missing():
    agent = TaskGuidanceAgent()

    # If the request is specific (e.g. read, locate), it should return the specific guidance,
    # NOT the generic "Please provide an image..." guidance, even when image is missing.
    guidance_read = agent.create_guidance(
        prompt="Read this medicine label.",
        image_provided=False,
    )
    assert any("visible text" in item for item in guidance_read)
    assert not any("provide an image" in item for item in guidance_read)

    guidance_locate = agent.create_guidance(
        prompt="Where is my phone?",
        image_provided=False,
    )
    assert any("Move slowly" in item for item in guidance_locate)
    assert not any("provide an image" in item for item in guidance_locate)