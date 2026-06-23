# Capstone Summary: Assistive Agent for Visually Impaired Users

## Track
Agents for Good

## Project Title
Assistive Agent for Visually Impaired Users

## Problem
Visually impaired users often need help understanding images, reading visible text, identifying objects, and completing daily tasks safely. A normal vision assistant may describe what it sees, but it can become unsafe if it gives overconfident navigation, medical, legal, or emergency guidance.

## Solution
This project is a safe, multi-agent assistive AI system built in Google Antigravity. The assistant can describe images, read visible text, provide cautious task guidance, refuse unsafe decisions, and log/evaluate its behavior.

## Target Users
- Visually impaired users
- Blind users
- Elderly users with reduced vision
- Caregivers
- Accessibility-focused organizations

## Architecture
The system uses an ADK-style multi-agent architecture:

1. Orchestrator Agent  
   Coordinates the full workflow.

2. Safety Agent  
   Detects medical, physical safety, privacy, legal, and financial risk.

3. Vision Agent  
   Uses Gemini vision when available and falls back to safe deterministic behavior.

4. OCR Agent  
   Reads visible text using Gemini vision when available and falls back safely.

5. Task Guidance Agent  
   Provides simple, cautious, everyday guidance.

6. Response Agent  
   Produces short, voice-friendly, screen-reader-friendly final responses.

## Course Concepts Demonstrated

### 1. Multi-Agent Systems
The project uses specialized agents coordinated by an Orchestrator Agent.

### 2. Agent Development Kit Style
The code follows an ADK-style design with agent classes, typed models, orchestration, and tests.

### 3. Agent Skills
Reusable skills are stored in `.agent/skills/`:
- scene-description
- text-reading
- accessibility-response
- safety-check

### 4. MCP Concepts
The project includes an MCP readiness layer:
- `agents/mcp_policy.py`
- `specs/mcp_plan.md`

This demonstrates least-privilege tool governance, read-only defaults, and confirmation requirements for write/export actions.

### 5. Security Features
The project includes:
- medical/legal/financial refusal logic
- physical safety caution
- privacy caution
- no hardcoded API keys
- no image-content logging
- human-in-the-loop policy
- safe fallback when Gemini fails

### 6. Evaluation
The project includes:
- evaluation dataset
- evaluation runner
- JSON report output
- tests validating evaluation behavior

### 7. Observability
The project logs:
- prompt
- whether an image was provided
- risk level
- safety action
- uncertainty
- final answer

It does not log image contents.

### 8. Real Gemini Vision and OCR
The Vision Agent and OCR Agent use Gemini image understanding when a valid API key is configured. If credentials fail or are missing, the system falls back safely instead of crashing.

## Demo Commands

Run all tests:
```bash
pytest
```

Run the offline evaluation suite:
```bash
python3 -m evaluation.run_evaluation
```

Run CLI interactive demo:
```bash
python3 -m app.cli "Read this sign" --image Stop-sign.jpg
```

## Current Limitations & Future Improvements

### Current Limitations
1. **Keyword Fallback Matching**: When live Gemini access keys are not present, specialized agents rely on mock responses keyed to prompts (e.g. `desk`, `phone`, `medicine`).
2. **Local Logging**: Logs and reports are currently stored in local JSON/JSONL files instead of external databases.

### Future Improvements
1. **Live External MCP Connections**: Connect to active, sandbox-restricted MCP servers for file reads, exports, and Drive syncing.
2. **Voice Streaming Integration**: Support full audio input/output streams for completely eyes-free operation.
3. **Mobile & Wearable Clients**: Connect to smart glasses or smartphone frontends for real-time situational assistance.