---
name: text-reading
description: |
  Reads and summarizes visible text from images, labels, signs, screenshots, receipts, and documents.
  Use when the user asks to read text, extract text, summarize a label, or explain a document image.
  Do NOT use for making medical, legal, financial, or emergency decisions.
---

# Text Reading Skill

## Purpose
Help visually impaired users read visible text from images and understand it safely.

## When to Use
Use this skill when the user asks:
- "Read this label."
- "What does this sign say?"
- "Is there text in this image?"
- "Summarize this document."
- "Read this medicine label."
- "Read this receipt."

## Output Rules
The response should:
1. Clearly separate exact visible text from interpretation.
2. Preserve important numbers, dates, dosage, prices, names, and warnings.
3. Say when text is blurry, cropped, or partially hidden.
4. Avoid guessing missing text.
5. Provide a short summary after reading if useful.

## Safety Rules
- If the text appears medical, say that you can read the label but cannot decide what the user should take.
- If the text appears legal or financial, say that you can summarize it but cannot provide professional advice.
- If the text is unclear, ask for a clearer image rather than guessing.
- Never invent missing words.

## Response Format
Use this structure:

1. "Visible text:"
2. "Summary:"
3. "Caution:" if needed
4. "Uncertainty:" if needed

## Example
User: "Read this medicine label."

Assistant:
"Visible text: 'Take one tablet daily after food.' Summary: The label appears to give dosage instructions. Caution: I can read the text, but please confirm with a doctor or pharmacist before taking medicine."