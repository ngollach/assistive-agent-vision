from agents.models import AgentResult, FinalResponse, RequiredAction, RiskLevel


class ResponseAgent:
    """Creates short, accessible, voice-friendly final responses."""

    def create_response(self, result: AgentResult) -> FinalResponse:
        safety = result.safety

        if safety and safety.required_action == RequiredAction.REFUSE:
            return FinalResponse(
                answer=self._build_refusal_response(result),
                risk_level=safety.risk_level,
                uncertainty=self._collect_uncertainty(result),
            )

        answer_parts: list[str] = []

        if result.vision:
            if result.vision.summary:
                answer_parts.append(result.vision.summary)

            if result.vision.spatial_details:
                answer_parts.append(" ".join(result.vision.spatial_details))

            if result.vision.possible_hazards:
                answer_parts.append(
                    "Caution: " + " ".join(result.vision.possible_hazards)
                )

        if result.ocr:
            if result.ocr.visible_text:
                answer_parts.append(f"Visible text: {result.ocr.visible_text}")

            if result.ocr.summary:
                answer_parts.append(f"Summary: {result.ocr.summary}")

        if safety and safety.required_action == RequiredAction.CAUTION:
            if safety.caution_message:
                answer_parts.append(f"Caution: {safety.caution_message}")
        if result.task_guidance:
            answer_parts.append("Guidance: " + " ".join(result.task_guidance))

        uncertainty = self._collect_uncertainty(result)
        if uncertainty:
            answer_parts.append(f"Uncertainty: {uncertainty}")

        if not answer_parts:
            answer_parts.append(
                "I do not have enough information to answer that safely."
            )

        return FinalResponse(
            answer=" ".join(answer_parts),
            risk_level=safety.risk_level if safety else RiskLevel.LOW,
            uncertainty=uncertainty,
        )

    def _build_refusal_response(self, result: AgentResult) -> str:
        safety = result.safety

        answer_parts = []

        if result.ocr and result.ocr.visible_text:
            answer_parts.append(f"Visible text: {result.ocr.visible_text}")

        if safety and safety.caution_message:
            answer_parts.append(safety.caution_message)
        else:
            answer_parts.append(
                "I cannot safely help with that request. Please verify with a qualified person."
            )

        return " ".join(answer_parts)

    @staticmethod
    def _collect_uncertainty(result: AgentResult) -> str | None:
        uncertainties = []

        if result.vision and result.vision.uncertainty:
            uncertainties.append(result.vision.uncertainty)

        if result.ocr and result.ocr.uncertainty:
            uncertainties.append(result.ocr.uncertainty)

        return " ".join(uncertainties) if uncertainties else None