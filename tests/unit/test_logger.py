import json

from agents.logger import AgentLogger
from agents.models import (
    FinalResponse,
    RequiredAction,
    RiskLevel,
    SafetyFinding,
    UserRequest,
)


def test_agent_logger_writes_jsonl_event(tmp_path):
    log_file = tmp_path / "agent_events.jsonl"

    logger = AgentLogger(log_path=str(log_file))

    request = UserRequest(
        prompt="Describe this image.",
        image_path="sample.jpg",
    )

    safety = SafetyFinding(
        risk_level=RiskLevel.LOW,
        reason="No high-risk category detected.",
        required_action=RequiredAction.ALLOW,
    )

    response = FinalResponse(
        answer="I see a table.",
        risk_level=RiskLevel.LOW,
    )

    logger.log_interaction(
        request=request,
        safety=safety,
        response=response,
    )

    lines = log_file.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 1

    event = json.loads(lines[0])

    assert event["prompt"] == "Describe this image."
    assert event["image_provided"] is True
    assert event["risk_level"] == "low"
    assert event["required_action"] == "allow"
    assert event["final_answer"] == "I see a table."