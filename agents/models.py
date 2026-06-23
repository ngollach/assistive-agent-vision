from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RequiredAction(str, Enum):
    ALLOW = "allow"
    CAUTION = "caution"
    REFUSE = "refuse"
    ASK_CONFIRMATION = "ask_confirmation"


class UserRequest(BaseModel):
    """Input received from the user."""

    prompt: str = Field(..., description="The user's question or instruction.")
    image_path: Optional[str] = Field(
        default=None,
        description="Optional local image path for prototype testing.",
    )


class VisionFinding(BaseModel):
    """Structured output from the Vision Agent."""

    summary: str
    objects: List[str] = Field(default_factory=list)
    spatial_details: List[str] = Field(default_factory=list)
    possible_hazards: List[str] = Field(default_factory=list)
    uncertainty: Optional[str] = None


class OCRFinding(BaseModel):
    """Structured output from the OCR Agent."""

    visible_text: str = ""
    summary: str = ""
    important_values: List[str] = Field(default_factory=list)
    uncertainty: Optional[str] = None


class SafetyFinding(BaseModel):
    """Structured output from the Safety Agent."""

    risk_level: RiskLevel
    reason: str
    required_action: RequiredAction
    caution_message: Optional[str] = None


class AgentResult(BaseModel):
    """Combined result passed to the Response Agent."""

    user_request: UserRequest
    vision: Optional[VisionFinding] = None
    ocr: Optional[OCRFinding] = None
    safety: Optional[SafetyFinding] = None
    task_guidance: List[str] = Field(default_factory=list)


class FinalResponse(BaseModel):
    """Final accessible response returned to the user."""

    answer: str
    risk_level: RiskLevel = RiskLevel.LOW
    uncertainty: Optional[str] = None