import base64
import tempfile
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents.orchestrator_agent import OrchestratorAgent


app = FastAPI(title="Live Assist Vision Agent")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class FrameRequest(BaseModel):
    image_base64: str
    prompt: str = (
        "Live assist mode: describe important objects, obstacles, text, or hazards. "
        "Use cautious language. Do not guarantee navigation safety."
    )


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/analyze-frame")
def analyze_frame(request: FrameRequest):
    image_data = request.image_base64

    if "," in image_data:
        image_data = image_data.split(",", 1)[1]

    try:
        frame_bytes = base64.b64decode(image_data)
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid base64 image data."},
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(frame_bytes)
            temp_path = temp_file.name

        agent = OrchestratorAgent()
        response = agent.handle_text_request(
            prompt=request.prompt,
            image_path=temp_path,
        )

        return {
            "answer": response.answer,
            "risk_level": response.risk_level.value,
            "uncertainty": response.uncertainty,
        }

    finally:
        if temp_path:
            try:
                Path(temp_path).unlink(missing_ok=True)
            except Exception:
                pass