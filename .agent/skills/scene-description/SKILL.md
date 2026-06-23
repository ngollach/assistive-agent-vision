---
name: scene-description
description: |
  Describes images, scenes, rooms, objects, layouts, and spatial relationships for visually impaired users.
  Use when the user asks what is in an image, what is in front of them, where an object is, or how a scene is arranged.
  Do NOT use for reading long text, medical decisions, legal advice, or guaranteed navigation instructions.
---

# Scene Description Skill

## Purpose
Help visually impaired users understand visual scenes through clear, short, and useful descriptions.

## When to Use
Use this skill when the user asks:
- "What is in front of me?"
- "Describe this image."
- "What objects are on the table?"
- "Where is my phone?"
- "What does this room look like?"

## Output Rules
The response should:
1. Start with the most important objects.
2. Mention approximate spatial relationships.
3. Use simple location terms such as left, right, center, front, back, near, far.
4. Mention hazards only if visible or likely from the image.
5. Clearly say when the image is unclear.
6. Avoid overclaiming certainty.

## Safety Rules
- Do not guarantee that a path is safe.
- Do not tell the user to walk, cross, or move quickly based only on an image.
- Do not identify people by name.
- Do not infer sensitive attributes about people.
- If the scene could involve physical safety, add a caution.

## Response Format
Use this structure:

1. Short summary.
2. Important details.
3. Safety caution if needed.
4. Uncertainty note if needed.

## Example
User: "What is in front of me?"

Assistant:
"I see a desk with a laptop in the center, a bottle near the front-right edge, and a notebook on the left. Be careful reaching forward because the bottle appears close to the edge."