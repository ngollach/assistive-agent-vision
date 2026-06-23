from agents.models import RequiredAction, RiskLevel, SafetyFinding, UserRequest


class SafetyAgent:
    """Checks user requests for safety, privacy, and high-impact risk."""

    MEDICAL_KEYWORDS = {
        "medicine",
        "medication",
        "tablet",
        "pill",
        "dose",
        "dosage",
        "prescription",
        "symptom",
        "diagnosis",
        "treatment",
        "doctor",
    }

    PHYSICAL_SAFETY_KEYWORDS = {
        "walk",
        "cross",
        "stairs",
        "road",
        "street",
        "traffic",
        "obstacle",
        "knife",
        "hot",
        "fire",
        "glass",
        "edge",
    }

    PRIVACY_KEYWORDS = {
        "id card",
        "passport",
        "license",
        "address",
        "bank",
        "face",
        "person name",
    }

    LEGAL_FINANCIAL_KEYWORDS = {
        "contract",
        "lawsuit",
        "legal",
        "bank",
        "investment",
        "loan",
        "tax",
        "insurance",
    }

    def analyze(self, request: UserRequest) -> SafetyFinding:
        prompt = request.prompt.lower()

        if self._contains_any(prompt, self.MEDICAL_KEYWORDS):
            return SafetyFinding(
                risk_level=RiskLevel.HIGH,
                reason="The request may involve medical information or a medical decision.",
                required_action=RequiredAction.REFUSE,
                caution_message=(
                    "I can help read visible text, but I cannot decide what medicine "
                    "you should take. Please confirm with a doctor or pharmacist."
                ),
            )

        if self._contains_any(prompt, self.PHYSICAL_SAFETY_KEYWORDS):
            return SafetyFinding(
                risk_level=RiskLevel.MEDIUM,
                reason="The request may involve physical safety or movement guidance.",
                required_action=RequiredAction.CAUTION,
                caution_message=(
                    "Use caution. I can describe visible information, but I cannot "
                    "guarantee that movement or navigation is safe."
                ),
            )

        if self._contains_any(prompt, self.PRIVACY_KEYWORDS):
            return SafetyFinding(
                risk_level=RiskLevel.MEDIUM,
                reason="The request may involve private or identifying information.",
                required_action=RequiredAction.CAUTION,
                caution_message=(
                    "I can help describe or read visible content, but I should not identify "
                    "people by name or expose private information."
                ),
            )

        if self._contains_any(prompt, self.LEGAL_FINANCIAL_KEYWORDS):
            return SafetyFinding(
                risk_level=RiskLevel.HIGH,
                reason="The request may involve legal or financial advice.",
                required_action=RequiredAction.REFUSE,
                caution_message=(
                    "I can summarize visible text, but I cannot provide legal or financial advice. "
                    "Please verify with a qualified professional."
                ),
            )

        return SafetyFinding(
            risk_level=RiskLevel.LOW,
            reason="No high-risk category detected.",
            required_action=RequiredAction.ALLOW,
            caution_message=None,
        )

    @staticmethod
    def _contains_any(text: str, keywords: set[str]) -> bool:
        return any(keyword in text for keyword in keywords)