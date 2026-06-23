# Project Instructions for Antigravity

## Project Name
Assistive Agent for Visually Impaired Users

## Development Style
Follow spec-driven development.

Before writing code:
1. Read `specs/project.md`.
2. Explain your understanding.
3. Propose a small implementation plan.
4. Wait for approval before making major changes.

## Core Rules
- Do not guess requirements.
- Do not create unnecessary features.
- Make the smallest useful change.
- Prefer clear, simple Python code.
- Keep files organized.
- Use readable names.
- Add comments only where helpful.
- Do not hardcode secrets or API keys.
- Do not store private user images unless explicitly approved.
- Use read-only tool access wherever possible.
- Ask for confirmation before write/export/share actions.

## Agentic Engineering Rules
- Think before coding.
- Use the project spec as the source of truth.
- When editing existing code, make surgical changes.
- Do not refactor unrelated code.
- Create tests for core behavior.
- Log important agent decisions.
- Prefer deterministic scripts for repeatable work.
- Keep responses accessible and voice-friendly.

## Safety Rules
This project serves visually impaired users, so safety is critical.

The assistant must:
- Avoid claiming certainty when image input is unclear.
- Avoid giving guaranteed navigation instructions.
- Avoid medical, legal, financial, or emergency decisions.
- Add caution when physical safety may be involved.
- Clearly say when it is uncertain.
- Recommend human verification for high-risk situations.
- Never identify people by name from images.

## Live Assist Development Rules
When implementing live camera or audio features:

- Treat the feature as a prototype demo, not a certified navigation system.
- Do not produce language that guarantees physical safety.
- Do not instruct the user to cross roads, walk into traffic, or move quickly.
- Prefer cautious language: "possible obstacle", "appears to be", "please verify".
- Always allow the user to start and stop the camera.
- Do not store video frames permanently.
- Do not log image contents.
- Keep frame analysis rate limited to avoid cost, latency, and noisy guidance.
- Use browser text-to-speech for demo audio output.

## Required Agents
The system should include:

1. Orchestrator Agent
2. Vision Agent
3. OCR Agent
4. Safety Agent
5. Task Guidance Agent
6. Response Agent

## Required Skills
The project should include these agent skills:

1. scene-description
2. text-reading
3. accessibility-response
4. safety-check

## Folder Structure
Use this structure:

```text
assistive-agent-vision/
├── specs/
│   └── project.md
├── .gemini/
│   └── GEMINI.md
├── .agent/
│   └── skills/
├── agents/
├── app/
├── tests/
├── evaluation/
├── logs/
├── requirements.txt
└── README.md