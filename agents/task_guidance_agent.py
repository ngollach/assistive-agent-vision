from agents.models import RequiredAction, RiskLevel, SafetyFinding


class TaskGuidanceAgent:
    """Provides safe, simple task guidance for visually impaired users."""

    def create_guidance(
        self,
        prompt: str,
        safety: SafetyFinding | None = None,
        image_provided: bool = False,
    ) -> list[str]:
        prompt_lower = prompt.lower()

        if safety and safety.required_action == RequiredAction.REFUSE:
            return [
                "I cannot safely guide that action.",
                "Please verify with a qualified person or trusted helper.",
            ]

        if "find" in prompt_lower or "where" in prompt_lower or "locate" in prompt_lower:
            return [
                "Move slowly and carefully.",
                "Use the object description and approximate location only as a guide.",
                "Confirm with touch or another trusted method before acting.",
            ]

        if "organize" in prompt_lower:
            return [
                "Start with one small area.",
                "Group similar items together.",
                "Keep frequently used items in a consistent place.",
            ]

        if "medicine" in prompt_lower or "medical" in prompt_lower:
            return [
                "Use the visible text as a reference.",
                "Please verify medicine instructions with a doctor or pharmacist.",
            ]

        if "contract" in prompt_lower or "bank" in prompt_lower or "legal" in prompt_lower or "financial" in prompt_lower:
            return [
                "Use the visible text as a reference.",
                "Please verify legal or financial content with a qualified professional.",
            ]

        if "read" in prompt_lower or "label" in prompt_lower or "sign" in prompt_lower:
            return []

        if safety and safety.risk_level == RiskLevel.MEDIUM:
            return [
                "Proceed carefully.",
                "Treat the response as helpful context, not a safety guarantee.",
            ]

        if not image_provided:
            return [
                "Please provide an image and a specific question.",
            ]

        return []