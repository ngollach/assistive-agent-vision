from agents.models import RiskLevel
from agents.orchestrator_agent import OrchestratorAgent


def test_orchestrator_describes_scene():
    agent = OrchestratorAgent()

    response = agent.handle_text_request(
        prompt="Describe this desk.",
        image_path="desk.jpg",
    )

    assert response.risk_level == RiskLevel.LOW
    assert "desk" in response.answer.lower() or "table" in response.answer.lower()


def test_orchestrator_reads_label():
    agent = OrchestratorAgent()

    response = agent.handle_text_request(
        prompt="Read this label.",
        image_path="label.jpg",
    )

    assert response.risk_level == RiskLevel.LOW
    assert "Visible text" in response.answer
    assert "Take one tablet" in response.answer


def test_orchestrator_refuses_medical_decision_but_reads_text():
    agent = OrchestratorAgent()

    response = agent.handle_text_request(
        prompt="Should I take this medicine?",
        image_path="medicine.jpg",
    )

    assert response.risk_level == RiskLevel.HIGH
    assert "Visible text" in response.answer
    assert "cannot decide" in response.answer


def test_orchestrator_handles_missing_image():
    agent = OrchestratorAgent()

    response = agent.handle_text_request(
        prompt="Describe this image.",
    )

    assert "No image was provided" in response.answer
    assert response.uncertainty is not None

def test_orchestrator_includes_task_guidance_for_object_location():
    agent = OrchestratorAgent()

    response = agent.handle_text_request(
        prompt="Where is my phone?",
        image_path="phone.jpg",
    )

    assert "Guidance:" in response.answer
    assert "Move slowly" in response.answer

def test_orchestrator_logs_interaction(tmp_path):
    agent = OrchestratorAgent()
    agent.logger.log_path = tmp_path / "agent_events.jsonl"

    response = agent.handle_text_request(
        prompt="Describe this desk.",
        image_path="desk.jpg",
    )

    assert response.answer

    log_text = agent.logger.log_path.read_text(encoding="utf-8")

    assert "Describe this desk." in log_text
    assert "risk_level" in log_text