# Assistive Agent for Visually Impaired Users

## Track
Agents for Good

## Project Overview
This project is a multi-agent assistive AI system for visually impaired users. It helps users understand images, read visible text, identify objects, and receive safe, voice-friendly guidance for everyday tasks.

The project was built in Google Antigravity using spec-driven development, agent skills, safety guardrails, evaluation, logging, and an ADK-style multi-agent architecture.

## Problem Statement
Visually impaired users often need help understanding their surroundings, reading labels or signs, identifying objects, and completing daily tasks. Existing tools may be fragmented or unsafe when they give overconfident answers about medical, navigation, or physical safety situations.

This project provides a safe assistive agent that gives clear descriptions, reads visible text, communicates uncertainty, and refuses high-risk decisions.

## Key Features
- Scene description from image prompts
- Text reading from labels, signs, receipts, and documents
- Safe object-location guidance
- Medical/legal/financial safety refusal behavior
- Voice-friendly accessible responses
- Human-in-the-loop design rules
- JSONL logging for observability
- Evaluation dataset and report generation
- CLI demo for capstone presentation

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
 │     └── Describes images and spatial relationships
 │
 ├── OCR Agent
 │     └── Reads visible text from image-based inputs
 │
 ├── Task Guidance Agent
 │     └── Provides safe everyday guidance
 │
 └── Response Agent
       └── Produces concise, screen-reader-friendly responses
```

## Course Concepts Demonstrated

1. **Multi-Agent Systems & Coordination:** Uses a hub-and-spoke Orchestrator Agent model to dynamically route visual and textual sub-tasks to Vision and OCR specialist agents.
2. **Agent Skills Design:** Implements specialized capabilities for scene description, text reading, accessibility formatting, and safety checks conforming to the skill specs.
3. **Security & Safety Guardrails:** Uses a deterministic Safety Agent that intercepts high-risk categories (medical, physical danger, privacy, legal/financial) to enforce caution warnings and hard refusals.
4. **Offline Programmatic Evaluation:** Evaluates agent capabilities against a baseline dataset, checking for correctness, required phrases, and forbidden safety violations.
5. **Observability Logging:** Records user prompts, risk levels, safety reasoning, and final answers in a local JSONL format for debugging without third-party APIs.

## Capstone Requirement Mapping

| Requirement | Implementation in This Project |
|---|---|
| Track | Agents for Good |
| Antigravity | Project developed and iterated inside Google Antigravity |
| Multi-Agent System / ADK-style architecture | Orchestrator Agent coordinates Safety, Vision, OCR, Task Guidance, and Response agents |
| Agent Skills | Skills stored under `.agent/skills/`: scene-description, text-reading, accessibility-response, safety-check |
| MCP Servers / MCP Concepts | `agents/mcp_policy.py` and `specs/mcp_plan.md` demonstrate safe MCP-style tool governance |
| Security Features | Safety Agent, MCP policy, no image-content logging, no hardcoded secrets, high-risk refusal behavior |
| Human-in-the-Loop | Required before write/export/share actions and high-risk tool usage |
| Evaluation | `evaluation/run_evaluation.py` and `assistive_eval_dataset.json` validate behavior |
| Observability | `logs/agent_events.jsonl` and `logs/evaluation_report.json` |
| Real Gemini Integration | Vision Agent and OCR Agent use Gemini when API credentials are available, with deterministic fallback |
| Real-world usefulness | Helps visually impaired users understand images, read text, and receive safe guidance |

## Setup Instructions

1. **Initialize and Activate Virtual Environment:**
   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## CLI Demo Commands

You can run the interactive CLI demo directly from your terminal:

```bash
# 1. Describe a scene (Low Risk)
python3 -m app.cli "Describe this desk." --image sample-desk.jpg

# 2. Locate an object (Medium Risk / Caution Guidance)
python3 -m app.cli "Where is my phone?" --image phone.jpg

# 3. Read a medicine label (High Risk / Refusal & Text Extraction)
python3 -m app.cli "Should I take this medicine?" --image medicine-label.jpg
```

## Evaluation Instructions

Run the local offline evaluation script to generate a compatibility and safety compliance report:

```bash
python3 -m evaluation.run_evaluation
```

* **Dataset:** [assistive_eval_dataset.json](file:///Users/nikhilgollachannu/Desktop/KaggleCapstone/assistive-agent-vision/evaluation/datasets/assistive_eval_dataset.json)
* **Output Report:** [evaluation_report.json](file:///Users/nikhilgollachannu/Desktop/KaggleCapstone/assistive-agent-vision/logs/evaluation_report.json)

## Safety Limitations

* **No Professional Advice:** The agent must never make medical, financial, or legal decisions.
* **No Navigation Guarantees:** Do not rely on spatial descriptions for physical obstacle avoidance or crossing roads.
* **No Identity Guessing:** The agent will not guess or infer private personal characteristics or identify individuals by name.

## Current Prototype Limitations

* **Deterministic Mocking:** In this prototype phase, the OCR, Vision, and Task Guidance agents return deterministic responses based on prompt keywords (such as `desk`, `phone`, `medicine`, `receipt`).
* **Offline Mock Mode:** No calls are made to live Gemini models, allowing the codebase to build, run, and pass unit tests locally without requiring Google Application Default Credentials (ADC) or active billing. Live model integration will be added in a subsequent phase.

## Final Capstone Demo Script

### Demo Goal
Show that the assistant can help visually impaired users understand visual information safely.

### Demo Flow

1. Run tests.

```bash
pytest

## Run Web/Mobile UI

Start the Streamlit app:

```bash
streamlit run app/web_ui.py