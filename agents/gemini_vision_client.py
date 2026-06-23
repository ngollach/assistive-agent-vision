import os
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image

load_dotenv()


class GeminiVisionClient:
    """Small wrapper around Gemini multimodal image analysis.

    Uses Gemini Developer API with API-key auth by default.
    Falls back safely when credentials, model access, or API mode are invalid.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash-lite") -> None:
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.last_error: str | None = None

        # Force Developer API mode unless the user intentionally changes this later.
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "false"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def analyze_image(self, image_path: str, prompt: str) -> str:
        if not self.is_available():
            raise RuntimeError("GOOGLE_API_KEY or GEMINI_API_KEY is not configured.")

        image_file = Path(image_path)

        if not image_file.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        try:
            from google import genai

            client = genai.Client(api_key=self.api_key)
            image = Image.open(image_file)

            response = client.models.generate_content(
                model=self.model_name,
                contents=[prompt, image],
            )

            return response.text or ""

        except Exception as exc:
            self.last_error = str(exc)
            raise RuntimeError(
                "Gemini image analysis failed. Check that you are using a Gemini "
                "Developer API key from AI Studio, not Vertex-only OAuth mode. "
                f"Original error: {exc}"
            ) from exc