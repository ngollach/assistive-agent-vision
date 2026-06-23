from agents.models import RequiredAction, RiskLevel, UserRequest
from agents.safety_agent import SafetyAgent


def test_safety_agent_allows_low_risk_request():
    agent = SafetyAgent()

    result = agent.analyze(
        UserRequest(prompt="Describe this image.")
    )

    assert result.risk_level == RiskLevel.LOW
    assert result.required_action == RequiredAction.ALLOW


def test_safety_agent_flags_medical_request_as_high_risk():
    agent = SafetyAgent()

    result = agent.analyze(
        UserRequest(prompt="Should I take this medicine?")
    )

    assert result.risk_level == RiskLevel.HIGH
    assert result.required_action == RequiredAction.REFUSE
    assert "doctor or pharmacist" in result.caution_message


def test_safety_agent_flags_physical_safety_request_as_medium_risk():
    agent = SafetyAgent()

    result = agent.analyze(
        UserRequest(prompt="Can I walk forward and cross the street?")
    )

    assert result.risk_level == RiskLevel.MEDIUM
    assert result.required_action == RequiredAction.CAUTION
    assert "cannot guarantee" in result.caution_message


def test_safety_agent_flags_privacy_request_as_medium_risk():
    agent = SafetyAgent()

    result = agent.analyze(
        UserRequest(prompt="Can you read this passport?")
    )

    assert result.risk_level == RiskLevel.MEDIUM
    assert result.required_action == RequiredAction.CAUTION


def test_safety_agent_flags_legal_financial_request_as_high_risk():
    agent = SafetyAgent()

    result = agent.analyze(
        UserRequest(prompt="Is this loan contract good for me?")
    )

    assert result.risk_level == RiskLevel.HIGH
    assert result.required_action == RequiredAction.REFUSE