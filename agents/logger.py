import json
from datetime import datetime, timezone
from pathlib import Path

from agents.models import FinalResponse, SafetyFinding, UserRequest


class AgentLogger:
    """Simple JSONL logger for agent observability.

    This logger avoids storing image contents. It only records metadata,
    safety decisions, and final response text for evaluation/debugging.
    """

    def __init__(self, log_path: str = "logs/agent_events.jsonl") -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_interaction(
        self,
        request: UserRequest,
        safety: SafetyFinding | None,
        response: FinalResponse,
    ) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prompt": request.prompt,
            "image_provided": request.image_path is not None,
            "risk_level": response.risk_level.value,
            "required_action": safety.required_action.value if safety else None,
            "safety_reason": safety.reason if safety else None,
            "uncertainty": response.uncertainty,
            "final_answer": response.answer,
        }

        with self.log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")