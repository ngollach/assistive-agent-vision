from agents.gemini_vision_client import GeminiVisionClient
from agents.models import UserRequest, VisionFinding


class VisionAgent:
    """Vision Agent for describing image-based scenes."""

    def __init__(self, vision_client: GeminiVisionClient | None = None) -> None:
        self.vision_client = vision_client or GeminiVisionClient()

    def analyze(self, request: UserRequest) -> VisionFinding:
        if not request.image_path:
            return VisionFinding(
                summary="No image was provided.",
                objects=[],
                spatial_details=[],
                possible_hazards=[],
                uncertainty="I need an image to describe the scene.",
            )

        if self.vision_client.is_available():
            return self._analyze_with_gemini(request)

        return self._fallback_analyze(request)

    def _analyze_with_gemini(self, request: UserRequest) -> VisionFinding:
        gemini_prompt = f"""
You are assisting a visually impaired user.

User request:
{request.prompt}

Analyze the image and return a concise scene description.

Rules:
- Mention important visible objects.
- Mention approximate spatial relationships.
- Mention visible hazards if any.
- Do not identify people by name.
- Do not infer sensitive traits.
- Do not guarantee navigation safety.
- Say when uncertain.
- Keep the answer short and voice-friendly.
"""

        try:
            text = self.vision_client.analyze_image(
                image_path=request.image_path or "",
                prompt=gemini_prompt,
            )
        except Exception as exc:
            fallback = self._fallback_analyze(request)
            fallback.uncertainty = (
                "Gemini vision failed, so I used the local prototype fallback. "
                f"Reason: {exc}"
            )
            return fallback

        return VisionFinding(
            summary=text.strip(),
            objects=[],
            spatial_details=[],
            possible_hazards=[],
            uncertainty=None,
        )

    def _fallback_analyze(self, request: UserRequest) -> VisionFinding:
        prompt = request.prompt.lower()

        if "desk" in prompt or "table" in prompt:
            return VisionFinding(
                summary="I see a desk or table-like surface with common objects.",
                objects=["desk or table", "object"],
                spatial_details=["Some objects may be on the surface."],
                possible_hazards=[],
                uncertainty=(
                    "This is a prototype response. Real image understanding "
                    "will be used when GOOGLE_API_KEY is configured."
                ),
            )

        if "phone" in prompt:
            return VisionFinding(
                summary="I can help look for a phone in the image.",
                objects=["phone"],
                spatial_details=[
                    "The exact location requires real image analysis."
                ],
                possible_hazards=[],
                uncertainty=(
                    "This prototype cannot truly inspect the image without GOOGLE_API_KEY."
                ),
            )

        return VisionFinding(
            summary="I can help describe the image, but real image analysis is not connected.",
            objects=[],
            spatial_details=[],
            possible_hazards=[],
            uncertainty=(
                "This prototype cannot truly inspect the image without GOOGLE_API_KEY."
            ),
        )