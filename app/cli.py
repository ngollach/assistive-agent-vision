import argparse

from agents.orchestrator_agent import OrchestratorAgent


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assistive Agent CLI demo for visually impaired users."
    )

    parser.add_argument(
        "prompt",
        type=str,
        help="User request, such as 'Describe this desk' or 'Read this label'.",
    )

    parser.add_argument(
        "--image",
        type=str,
        default=None,
        help="Optional local image path for prototype testing.",
    )

    args = parser.parse_args()

    agent = OrchestratorAgent()
    response = agent.handle_text_request(
        prompt=args.prompt,
        image_path=args.image,
    )

    print("\nAssistive Agent Response:")
    print(response.answer)
    print(f"\nRisk level: {response.risk_level.value}")

    if response.uncertainty:
        print(f"Uncertainty: {response.uncertainty}")


if __name__ == "__main__":
    main()