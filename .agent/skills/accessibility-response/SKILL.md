---
name: accessibility-response
description: |
  Converts agent findings into short, clear, voice-friendly responses for visually impaired users.
  Use when the final answer needs to be accessible, concise, screen-reader-friendly, or spoken aloud.
  Do NOT use for raw technical debugging output.
---

# Accessibility Response Skill

## Purpose
Transform technical agent output into clear, helpful language suitable for screen readers and voice assistants.

## Response Principles
The final response should be:
- Short
- Clear
- Direct
- Voice-friendly
- Non-visual when possible
- Free of unnecessary formatting
- Honest about uncertainty

## Writing Rules
1. Put the most useful information first.
2. Use short sentences.
3. Avoid large paragraphs.
4. Avoid complex visual-only explanations.
5. Avoid saying "as you can see."
6. Use directional words carefully.
7. Mention uncertainty clearly.
8. Include safety cautions when needed.

## Good Response Example
"I see a laptop in the center of the table, a phone to the left, and a cup near the front edge. Be careful with the cup because it may be easy to knock over."

## Bad Response Example
"The image contains several objects arranged aesthetically across a horizontal plane with visual balance and possible consumer electronics."

## Final Answer Structure
Use this structure when possible:

1. Main answer
2. Key details
3. Caution or uncertainty
4. Optional next step