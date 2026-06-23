import json
from pathlib import Path

from agents.orchestrator_agent import OrchestratorAgent


def phrase_found(answer: str, phrase: str) -> bool:
    return phrase.lower() in answer.lower()


def evaluate_dataset(dataset_path: str) -> dict:
    dataset_file = Path(dataset_path)
    cases = json.loads(dataset_file.read_text(encoding="utf-8"))

    agent = OrchestratorAgent()

    results = []
    passed = 0

    for case in cases:
        response = agent.handle_text_request(
            prompt=case["prompt"],
            image_path=case.get("image_path"),
        )

        answer = response.answer

        risk_level_passed = response.risk_level.value == case["expected_risk_level"]

        expected_phrase_passed = any(
            phrase_found(answer, phrase)
            for phrase in case["expected_phrases"]
        )

        forbidden_phrase_passed = all(
            not phrase_found(answer, phrase)
            for phrase in case["must_not_include"]
        )

        case_passed = (
            risk_level_passed
            and expected_phrase_passed
            and forbidden_phrase_passed
        )

        if case_passed:
            passed += 1

        results.append(
            {
                "id": case["id"],
                "passed": case_passed,
                "risk_level": response.risk_level.value,
                "risk_level_passed": risk_level_passed,
                "expected_phrase_passed": expected_phrase_passed,
                "forbidden_phrase_passed": forbidden_phrase_passed,
                "answer": answer,
            }
        )

    total = len(cases)

    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total else 0,
        "results": results,
    }


def main() -> None:
    dataset_path = "evaluation/datasets/assistive_eval_dataset.json"
    report = evaluate_dataset(dataset_path)

    output_path = Path("logs/evaluation_report.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))
    print(f"\nEvaluation report saved to: {output_path}")


if __name__ == "__main__":
    main()