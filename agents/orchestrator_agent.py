from agents.task_guidance_agent import TaskGuidanceAgent
from agents.models import AgentResult, FinalResponse, UserRequest
from agents.ocr_agent import OCRAgent
from agents.response_agent import ResponseAgent
from agents.safety_agent import SafetyAgent
from agents.vision_agent import VisionAgent
from agents.logger import AgentLogger

class OrchestratorAgent:
    """Coordinates specialist agents for the assistive vision workflow."""

    OCR_KEYWORDS = {
        "read",
        "text",
        "label",
        "sign",
        "document",
        "receipt",
        "medicine",
        "screenshot",
    }

    VISION_KEYWORDS = {
        "describe",
        "what is",
        "what's",
        "front",
        "object",
        "room",
        "desk",
        "table",
        "phone",
        "where",
        "image",
        "scene",
    }

    def __init__(self) -> None:
        self.safety_agent = SafetyAgent()
        self.vision_agent = VisionAgent()
        self.ocr_agent = OCRAgent()
        self.response_agent = ResponseAgent()
        self.task_guidance_agent = TaskGuidanceAgent()
        self.logger = AgentLogger()

    def handle_request(self, request: UserRequest) -> FinalResponse:
        safety = self.safety_agent.analyze(request)

        should_run_ocr = self._should_run_ocr(request.prompt)
        should_run_vision = self._should_run_vision(request.prompt)

        vision = None
        ocr = None

        if should_run_vision:
            vision = self.vision_agent.analyze(request)

        if should_run_ocr:
            ocr = self.ocr_agent.analyze(request)

        task_guidance = self.task_guidance_agent.create_guidance(
            prompt=request.prompt,
            safety=safety,
            image_provided=request.image_path is not None,
        )

        result = AgentResult(
            user_request=request,
            vision=vision,
            ocr=ocr,
            safety=safety,
            task_guidance=task_guidance,
        )

        final_response = self.response_agent.create_response(result)

        self.logger.log_interaction(
            request=request,
            safety=safety,
            response=final_response,
        )

        return final_response

    def handle_text_request(
        self,
        prompt: str,
        image_path: str | None = None,
    ) -> FinalResponse:
        request = UserRequest(prompt=prompt, image_path=image_path)
        return self.handle_request(request)

    @classmethod
    def _should_run_ocr(cls, prompt: str) -> bool:
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in cls.OCR_KEYWORDS)

    @classmethod
    def _should_run_vision(cls, prompt: str) -> bool:
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in cls.VISION_KEYWORDS)