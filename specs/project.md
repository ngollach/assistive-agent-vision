# Assistive Agent for Visually Impaired Users

## Track
Agents for Good

## Project Summary
This project is a multi-agent assistive AI system for visually impaired users. It helps users understand images, read visible text, identify objects, and receive safe, voice-friendly guidance for everyday tasks.

The system will be built using Google Antigravity and Google Agent Development Kit principles. It will demonstrate multi-agent design, agent skills, MCP-style tool integration, security guardrails, human-in-the-loop confirmation, and evaluation.

## Problem Statement
Visually impaired users often need help understanding their surroundings, reading signs, reading labels, identifying objects, and completing daily tasks. Existing tools may be limited, fragmented, or unsafe when they give confident answers about high-risk situations.

This project aims to provide a safe and useful AI assistant that can explain visual information clearly while avoiding unsafe claims.

## Target Users
- Visually impaired users
- Blind users
- Elderly users with reduced vision
- Caregivers assisting visually impaired people
- Accessibility-focused organizations

## Core User Inputs
The user may provide:
- An uploaded image
- A screenshot
- A document image
- A camera-style scene image
- A text question about the image

Example prompts:
- "What is in front of me?"
- "Read this label."
- "Describe this room."
- "What objects are on this table?"
- "Is there any text in this image?"
- "Help me understand this document."

## Core Outputs
The assistant should return:
- A short voice-friendly answer
- Important objects or text detected
- Safety warnings when needed
- A confidence note when uncertain
- Follow-up guidance only when safe

Example output:

"I see a table with a laptop, a water bottle, and a notebook. The water bottle appears close to the front-right edge of the table, so be careful if reaching forward."

## Main Features
1. Scene description from uploaded images.
2. Text reading from labels, signs, documents, or screenshots.
3. Object and environment explanation.
4. Safety-aware response generation.
5. Voice-friendly concise answers.
6. Human-in-the-loop confirmation for risky tasks.
7. Logging for evaluation and debugging.

## Agents

### 1. Orchestrator Agent
Coordinates the full workflow. It receives the user request, decides which specialist agents to call, combines their results, and sends the final response.

### 2. Vision Agent
Analyzes images and describes visible objects, people, surroundings, layouts, and spatial relationships.

### 3. OCR Agent
Extracts and summarizes visible text from images, signs, labels, screenshots, and document photos.

### 4. Safety Agent
Checks whether the response involves risky areas such as medical, legal, financial, navigation-critical, emergency, or physical safety decisions.

### 5. Task Guidance Agent
Provides simple step-by-step help for safe everyday tasks, such as locating objects, understanding a label, or organizing information.

### 6. Response Agent
Converts technical findings into clear, short, accessible, screen-reader-friendly language.

## Agent Skills

### scene-description
Used when the user asks the assistant to describe an image, room, object, or environment.

### text-reading
Used when the user asks the assistant to read labels, signs, screenshots, documents, or visible text.

### accessibility-response
Used when the assistant needs to produce voice-friendly, concise, accessible responses.

### safety-check
Used when the assistant must check for risk, uncertainty, or human confirmation requirements.

## MCP / Tool Integrations

The project may use MCP-style integrations for:
- File or image input
- Local filesystem access during development
- Google Drive for optional report storage
- Google Docs for optional generated summaries
- Search only if the user asks for public information

Security rule:
All external tools should use least-privilege access. Write actions require user confirmation.

## Security and Safety Requirements
1. Do not claim certainty when the image is unclear.
2. Do not provide medical, legal, financial, or emergency decisions.
3. Do not provide navigation-critical instructions as guaranteed safe.
4. Warn the user when physical safety may be involved.
5. Ask for confirmation before saving, sharing, or exporting user data.
6. Avoid storing private images unless the user explicitly approves.
7. Use read-only access wherever possible.
8. Log agent actions for evaluation, but do not log sensitive image contents unnecessarily.

## Human-in-the-Loop Rules
The assistant must ask for confirmation before:
- Saving user images
- Exporting summaries
- Sending data to external tools
- Giving high-impact recommendations
- Performing write actions through MCP tools

## BDD Scenarios

### Scenario 1: Describe a simple scene
Given the user uploads an image of a desk
When the user asks "What is in front of me?"
Then the Vision Agent identifies major objects
And the Response Agent gives a short, voice-friendly description

### Scenario 2: Read visible text
Given the user uploads an image of a label
When the user asks "Read this label"
Then the OCR Agent extracts visible text
And the Safety Agent checks whether the label involves medical or safety-sensitive content
And the Response Agent returns the text with an uncertainty warning if needed

### Scenario 3: Safety warning for medicine label
Given the user uploads an image of a medicine label
When the user asks "Should I take this?"
Then the assistant reads visible text only
And refuses to make a medical decision
And recommends confirming with a doctor or pharmacist

### Scenario 4: Unclear image
Given the uploaded image is blurry
When the user asks for a description
Then the assistant explains that the image is unclear
And provides only high-confidence observations
And asks the user to upload a clearer image if needed

### Scenario 5: Object location guidance
Given the user uploads an image of a table
When the user asks "Where is my phone?"
Then the Vision Agent identifies likely phone location
And the Response Agent describes the location using simple spatial language
And the Safety Agent adds caution if the object is near an edge or hazard

## Evaluation Metrics
The project will be evaluated using:

1. Scene description accuracy
2. OCR accuracy
3. Safety compliance
4. Response clarity
5. Tool-call success rate
6. Hallucination rate
7. User usefulness score

## Success Criteria
The capstone is successful if:
- The system uses at least 3 course concepts.
- The system demonstrates a working multi-agent workflow.
- The system includes at least 3 agent skills.
- The system includes safety checks.
- The system includes evaluation tests.
- The final output is useful for visually impaired users.

## Out of Scope
This project will not:
- Replace professional medical advice
- Replace emergency services
- Guarantee safe physical navigation
- Identify people by name
- Store private images without permission

## Demo Plan
The final demo will show:
1. User uploads a room or desk image.
2. Assistant describes the scene.
3. User uploads a label image.
4. Assistant reads the label.
5. User asks a risky question.
6. Safety Agent blocks unsafe advice.
7. Final response is accessible and voice-friendly.