# Assistive Agent for Visually Impaired Users

## Track

Agents for Good

## Project Overview

This project is a multi-agent assistive AI system for visually impaired users. It helps users understand images, read visible text, identify objects, receive safe task guidance, and use live camera assistance with spoken feedback.

The project was built in Google Antigravity using spec-driven development, agent skills, safety guardrails, evaluation, logging, Gemini multimodal vision, and an ADK-style multi-agent architecture.

## Problem Statement

Visually impaired users often need help understanding their surroundings, reading signs or labels, identifying objects, and completing daily tasks safely. Existing tools may be fragmented or unsafe when they give overconfident answers about medical, navigation, emergency, or physical safety situations.

This project provides a safe assistive agent that gives clear descriptions, reads visible text, communicates uncertainty, refuses high-risk decisions, and provides cautious voice-friendly guidance.

## Target Users

* Visually impaired users
* Blind users
* Elderly users with reduced vision
* Caregivers
* Accessibility-focused organizations

## Key Features

* Scene description from image prompts
* Text reading from signs, labels, receipts, screenshots, and documents
* Safe object-location guidance
* Medical, legal, and financial safety refusal behavior
* Voice-friendly accessible responses
* Live camera assist mode
* Browser audio guidance using text-to-speech
* Human-in-the-loop design rules
* JSONL logging for observability
* Evaluation dataset and report generation
* CLI demo
* Streamlit web/mobile UI
* FastAPI live assist camera page
* MCP readiness and tool-governance layer

## Multi-Agent Architecture

```text
User
 │
Orchestrator Agent
 │
 ├── Safety Agent
 │     └── Detects medical, physical safety, privacy, legal, and financial risks
 │
 ├── Vision Agent
 │     └── Describes images and spatial relationships using Gemini vision when available
 │
 ├── OCR Agent
 │     └── Reads visible text from image-based inputs using Gemini vision when available
 │
 ├── Task Guidance Agent
 │     └── Provides safe everyday guidance
 │
 └── Response Agent
       └── Produces concise, screen-reader-friendly responses
```

## Live Assist Architecture

```text
Browser Camera
   ↓
JavaScript video stream
   ↓
Frame captured every few seconds
   ↓
POST frame to FastAPI backend
   ↓
Orchestrator Agent
   ↓
Vision / OCR / Safety / Task Guidance / Response Agents
   ↓
Browser displays response
   ↓
Browser speaks response using text-to-speech
```

## Course Concepts Demonstrated

### 1. Multi-Agent System

The system uses multiple specialized agents:

* `SafetyAgent`
* `VisionAgent`
* `OCRAgent`
* `TaskGuidanceAgent`
* `ResponseAgent`
* `OrchestratorAgent`

### 2. ADK-Style Architecture

The project follows an ADK-style agent design with:

* typed data models
* specialist agent classes
* orchestrated workflow
* testable agent behavior
* clear separation of responsibilities

### 3. Agent Skills

The project includes reusable skills under:

```text
.agent/skills/
```

Skills included:

* `scene-description`
* `text-reading`
* `accessibility-response`
* `safety-check`
* `live-assist`

### 4. Spec-Driven Development

The main project specification lives in:

```text
specs/project.md
```

The Antigravity project instructions live in:

```text
.gemini/GEMINI.md
```

This follows the workflow:

```text
Spec → Plan → Build → Test → Evaluate
```

### 5. Gemini Multimodal LLM

The project uses Gemini vision for:

* image description
* scene understanding
* OCR-style visible text reading
* live camera frame analysis

If the Gemini API key is missing or invalid, the system falls back to deterministic local behavior so tests and demos do not crash.

### 6. MCP Readiness and Tool Governance

The project includes an MCP readiness layer:

```text
agents/mcp_policy.py
specs/mcp_plan.md
```

This demonstrates:

* least-privilege tool access
* read-only default behavior
* write/export blocking by default
* human confirmation before sensitive actions
* safe future integration with tools like Google Drive, Docs, Sheets, or filesystem access

### 7. Security and Safety

The system includes:

* medical decision refusal
* legal and financial advice refusal
* physical safety caution
* privacy caution
* no image-content logging
* no hardcoded secrets
* safe fallback when Gemini fails
* human-in-the-loop policy
* no guaranteed navigation claims
* no person identification by name

### 8. Logging and Observability

Agent interactions are logged to:

```text
logs/agent_events.jsonl
```

The logger records:

* prompt
* whether an image was provided
* risk level
* required safety action
* safety reason
* uncertainty
* final answer

It does not log raw image contents or video frames.

### 9. Evaluation

Evaluation dataset:

```text
evaluation/datasets/assistive_eval_dataset.json
```

Evaluation runner:

```text
evaluation/run_evaluation.py
```

Evaluation report output:

```text
logs/evaluation_report.json
```

Evaluation checks include:

* scene description behavior
* OCR label reading
* medical refusal
* missing image handling
* object-location guidance
* unsafe phrase prevention
* expected risk level

## Capstone Requirement Mapping

| Requirement                                 | Implementation in This Project                                                                       |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Track                                       | Agents for Good                                                                                      |
| Antigravity                                 | Project developed and iterated inside Google Antigravity                                             |
| Multi-Agent System / ADK-style architecture | Orchestrator Agent coordinates Safety, Vision, OCR, Task Guidance, and Response agents               |
| Agent Skills                                | Skills stored under `.agent/skills/`                                                                 |
| MCP Servers / MCP Concepts                  | `agents/mcp_policy.py` and `specs/mcp_plan.md` demonstrate safe MCP-style tool governance            |
| Security Features                           | Safety Agent, MCP policy, no image-content logging, no hardcoded secrets, high-risk refusal behavior |
| Human-in-the-Loop                           | Required before write/export/share actions and high-risk tool usage                                  |
| Evaluation                                  | `evaluation/run_evaluation.py` and `assistive_eval_dataset.json` validate behavior                   |
| Observability                               | `logs/agent_events.jsonl` and `logs/evaluation_report.json`                                          |
| Real-world usefulness                       | Helps visually impaired users understand images, read text, and receive safe guidance                |
| Advanced UI                                 | Streamlit web/mobile UI and FastAPI live camera assist mode                                          |
| Audio Guidance                              | Browser text-to-speech in Live Assist Mode                                                           |

## Project Structure

```text
assistive-agent-vision/
├── .agent/
│   └── skills/
│       ├── accessibility-response/
│       ├── live-assist/
│       ├── safety-check/
│       ├── scene-description/
│       └── text-reading/
├── .gemini/
│   └── GEMINI.md
├── agents/
│   ├── app_utils/
│   ├── gemini_vision_client.py
│   ├── logger.py
│   ├── mcp_policy.py
│   ├── models.py
│   ├── ocr_agent.py
│   ├── orchestrator_agent.py
│   ├── response_agent.py
│   ├── safety_agent.py
│   ├── task_guidance_agent.py
│   └── vision_agent.py
├── app/
│   ├── cli.py
│   ├── web_ui.py
│   └── live_assist/
│       ├── __init__.py
│       ├── server.py
│       └── static/
│           └── index.html
├── evaluation/
│   ├── datasets/
│   │   └── assistive_eval_dataset.json
│   └── run_evaluation.py
├── logs/
├── specs/
│   ├── mcp_plan.md
│   └── project.md
├── tests/
├── CAPSTONE_SUMMARY.md
├── README.md
├── requirements.txt
└── pytest.ini
```

## Setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a local `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=false
ENABLE_IMAGE_LOGGING=false
```

Important:

* Do not commit `.env`.
* Do not hardcode API keys.
* Use a Gemini Developer API key from Google AI Studio.
* Keep `GOOGLE_GENAI_USE_VERTEXAI=false` when using API-key mode.

Your `.gitignore` should include:

```gitignore
.env
```

## Run Tests

```bash
pytest
```

Expected:

```text
All unit tests pass.
Credential-dependent integration tests may be skipped.
```

## Run CLI Demo

### Demo 1: Scene Description

```bash
python3 -m app.cli "Describe this image" --image Stop-sign.jpg
```

Expected behavior:

* Uses Gemini vision if API key is configured
* Describes the image
* Gives a concise accessible response
* Shows risk level

Example:

```text
Assistive Agent Response:
This is a red octagonal stop sign with the word "STOP" in white capital letters across its face.

Risk level: low
```

### Demo 2: OCR / Text Reading

```bash
python3 -m app.cli "Read this sign" --image Stop-sign.jpg
```

Expected behavior:

* Reads or summarizes visible text
* May include text such as `STOP`
* Keeps answer voice-friendly

### Demo 3: Medical Safety Refusal

```bash
python3 -m app.cli "Should I take this medicine?" --image medicine-label.jpg
```

Expected behavior:

* May read visible text
* Refuses to make a medical decision
* Recommends confirming with a doctor or pharmacist

### Demo 4: Object Location Guidance

```bash
python3 -m app.cli "Where is my phone?" --image phone.jpg
```

Expected behavior:

* Gives phone-related response
* Adds safe guidance such as moving slowly and confirming with touch or another trusted method
* Does not guarantee physical safety

## Run Streamlit Web/Mobile UI

Start the Streamlit app:

```bash
streamlit run app/web_ui.py
```

The app opens in your browser.

The Streamlit UI supports:

* image upload
* user prompt input
* assistant response
* risk level display
* uncertainty warning
* privacy notice

### Mobile Testing for Streamlit

1. Make sure your laptop and phone are on the same Wi-Fi.
2. Copy the Network URL from the Streamlit terminal.
3. Open it on your phone browser.

## Run Live Assist Camera Demo

Start the FastAPI live assist server:

```bash
uvicorn app.live_assist.server:app --reload --port 8000
```

Open in browser:

```text
http://127.0.0.1:8000
```

The Live Assist page supports:

* browser camera access
* Start Live Assist
* Stop Live Assist
* Analyze Now
* automatic frame analysis every 5 seconds
* spoken guidance using browser text-to-speech
* risk level display
* uncertainty display
* safety notice

### Mobile Testing for Live Assist

Make sure your laptop and phone are on the same Wi-Fi.

Find your laptop IP:

```bash
ipconfig getifaddr en0
```

Open on your phone:

```text
http://YOUR_LAPTOP_IP:8000
```

Note: some mobile browsers require HTTPS for camera access unless the app is running on localhost. If mobile camera access fails, demo using the laptop browser.

## Run Evaluation

```bash
python3 -m evaluation.run_evaluation
```

Expected result:

```text
Total cases: 5
Passed cases: 5
Failed cases: 0
Pass rate: 100%
```

The evaluation report is saved to:

```text
logs/evaluation_report.json
```

## Final Capstone Demo Script

### Demo Goal

Show that the assistant can help visually impaired users understand visual information safely using both static image analysis and live camera guidance.

### Demo Flow

1. Run tests.

```bash
pytest
```

Expected:

```text
All unit tests pass.
Credential-dependent integration tests may be skipped.
```

2. Run CLI image description.

```bash
python3 -m app.cli "Describe this image" --image Stop-sign.jpg
```

Expected:

The assistant describes the stop sign using Gemini vision.

3. Run OCR/text reading.

```bash
python3 -m app.cli "Read this sign" --image Stop-sign.jpg
```

Expected:

The assistant reads or summarizes the visible text, such as `STOP`.

4. Run safety refusal.

```bash
python3 -m app.cli "Should I take this medicine?" --image medicine-label.jpg
```

Expected:

The assistant may read visible text but refuses to make a medical decision.

5. Run Streamlit web UI.

```bash
streamlit run app/web_ui.py
```

Expected:

The user can upload an image and ask a question from a browser/mobile-friendly interface.

6. Run Live Assist Mode.

```bash
uvicorn app.live_assist.server:app --reload --port 8000
```

Expected:

The browser camera opens, captures frames every few seconds, analyzes them, displays guidance, and speaks the response aloud.

7. Run evaluation.

```bash
python3 -m evaluation.run_evaluation
```

Expected:

Evaluation report is generated at:

```text
logs/evaluation_report.json
```

### Key Point to Explain

This project is not just a chatbot. It is an agentic system with specialized agents, reusable skills, Gemini multimodal vision, live camera assistance, safety checks, MCP-ready tool governance, logging, and evaluation.

## Current Prototype Limitations

* Live Assist Mode is a prototype demonstration.
* It is not a certified navigation aid.
* It should not be used as the only source of guidance while walking.
* Camera frames are analyzed periodically, not continuously.
* Mobile camera access may require HTTPS depending on the browser.
* Gemini output may vary depending on image quality and API availability.
* Full RAG is not implemented yet.
* A real MCP server is not connected yet; the project currently includes MCP readiness and governance.

## Future Improvements

* Add HTTPS support for easier mobile camera access
* Add real MCP Google Drive/Docs integration
* Add voice input
* Add stronger audio guidance controls
* Add object-distance estimation
* Add image-quality checks
* Add stronger evaluation datasets
* Add RAG for accessibility manuals, medicine safety guides, or user-specific instructions
* Add user-controlled privacy settings
* Add deployment instructions

## Safety Notice

This assistant does not replace professional medical, legal, financial, emergency, or navigation support.

Live Assist Mode is a prototype demonstration. It is not a certified navigation aid and should not be used as the only source of guidance while walking. Users should continue using a cane, guide dog, trusted helper, or professional mobility support.

The assistant should provide cautious assistance and clearly state uncertainty when visual input is unclear.
