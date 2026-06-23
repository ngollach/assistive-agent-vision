---
name: safety-check
description: |
  Checks whether an assistive response involves safety risk, uncertainty, privacy risk, or high-impact advice.
  Use before final responses involving navigation, medicine, legal, financial, emergency, physical safety, identity, or private data.
  Do NOT use as a replacement for professional judgment.
---

# Safety Check Skill

## Purpose
Prevent unsafe, overconfident, or privacy-invasive responses in an assistive agent for visually impaired users.

## Risk Categories
Check whether the user request involves:

1. Physical safety
   - walking
   - crossing roads
   - stairs
   - obstacles
   - sharp objects
   - hot surfaces
   - fragile items

2. Medical
   - medicine labels
   - symptoms
   - dosage
   - treatment
   - diagnosis

3. Legal or financial
   - contracts
   - bills
   - bank documents
   - investment decisions

4. Emergency
   - danger
   - injury
   - fire
   - crime
   - urgent help

5. Privacy
   - faces
   - IDs
   - addresses
   - private documents
   - personal images

6. Identity
   - identifying people by name
   - guessing age, ethnicity, religion, disability, or other sensitive traits

## Required Behavior
If risk is low:
- Allow the response.

If risk is medium:
- Add a caution.
- Mention uncertainty.
- Avoid guaranteed claims.

If risk is high:
- Refuse unsafe instruction.
- Provide safe alternative guidance.
- Recommend human or professional verification.

## Human-in-the-Loop Required Before
Ask for user confirmation before:
- Saving images
- Exporting documents
- Sending data externally
- Making write actions
- Acting on high-risk information

## Output Format
Return:

Risk level: low / medium / high

Reason:
Short explanation.

Required action:
allow / caution / refuse / ask confirmation

## Example
User: "Should I take this medicine?"

Safety result:
Risk level: high

Reason:
The request asks for a medical decision.

Required action:
Refuse medical decision. Read visible label text only and recommend confirming with a doctor or pharmacist.