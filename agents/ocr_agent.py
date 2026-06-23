from agents.gemini_vision_client import GeminiVisionClient
from agents.models import OCRFinding, UserRequest


class OCRAgent:
    """OCR Agent for reading visible text from images."""

    def __init__(self, vision_client: GeminiVisionClient | None = None) -> None:
        self.vision_client = vision_client or GeminiVisionClient()

    def analyze(self, request: UserRequest) -> OCRFinding:
        if not request.image_path:
            return OCRFinding(
                visible_text="",
                summary="No image was provided for text reading.",
                important_values=[],
                uncertainty="I need an image to read visible text.",
            )

        if self.vision_client.is_available():
            return self._analyze_with_gemini(request)

        return self._fallback_analyze(request)

    def _analyze_with_gemini(self, request: UserRequest) -> OCRFinding:
        gemini_prompt = f"""
You are assisting a visually impaired user.

User request:
{request.prompt}

Read the visible text in the image.

Return only plain text in this exact format:
Visible text: <exact visible text>
Summary: <one short sentence>
Important values: <comma-separated values or N/A>
Uncertainty: <short note or None>

Rules:
- Do not use Markdown or numbered lists in OCR output.
- Do not add extra headings.
- Do not invent missing text.
- Do not make medical, legal, or financial decisions.
- Keep the response short and voice-friendly.
"""

        try:
            text = self.vision_client.analyze_image(
                image_path=request.image_path or "",
                prompt=gemini_prompt,
            )
        except Exception as exc:
            fallback = self._fallback_analyze(request)
            fallback.uncertainty = (
                "Gemini OCR failed, so I used the local prototype fallback. "
                f"Reason: {exc}"
            )
            return fallback

        visible_text = ""
        summary = ""
        important_values = []
        uncertainty = None

        for line in text.splitlines():
            line = line.strip()
            if line.lower().startswith("visible text:"):
                visible_text = line[len("visible text:"):].strip()
            elif line.lower().startswith("summary:"):
                summary = line[len("summary:"):].strip()
            elif line.lower().startswith("important values:"):
                vals = line[len("important values:"):].strip()
                if vals and vals.lower() != "n/a":
                    important_values = [v.strip() for v in vals.split(",") if v.strip()]
            elif line.lower().startswith("uncertainty:"):
                unc = line[len("uncertainty:"):].strip()
                if unc and unc.lower() != "none":
                    uncertainty = unc

        if not visible_text:
            visible_text = text.strip()
        if not summary:
            summary = "Text extracted from image."

        return OCRFinding(
            visible_text=visible_text,
            summary=summary,
            important_values=important_values,
            uncertainty=uncertainty,
        )

    def _fallback_analyze(self, request: UserRequest) -> OCRFinding:
        prompt = request.prompt.lower()

        if "medicine" in prompt or "label" in prompt:
            return OCRFinding(
                visible_text="Take one tablet daily after food.",
                summary="The text provides dosage instructions.",
                important_values=["one tablet", "daily", "after food"],
                uncertainty=(
                    "This is prototype text. Real OCR will be used when GOOGLE_API_KEY "
                    "is configured."
                ),
            )

        if "receipt" in prompt:
            return OCRFinding(
                visible_text="Total: $12.50",
                summary="The text shows a receipt total.",
                important_values=["$12.50"],
                uncertainty=(
                    "This is prototype text. Real OCR will be used when GOOGLE_API_KEY "
                    "is configured."
                ),
            )

        if "sign" in prompt:
            return OCRFinding(
                visible_text="Exit",
                summary="The text is a short sign.",
                important_values=["Exit"],
                uncertainty=(
                    "This is prototype text. Real OCR will be used when GOOGLE_API_KEY "
                    "is configured."
                ),
            )

        return OCRFinding(
            visible_text="",
            summary="No readable text detected.",
            important_values=[],
            uncertainty=(
                "This prototype cannot truly inspect image text without GOOGLE_API_KEY."
            ),
        )