"""
Customer service bot example.

Demonstrates how to use UCEF for a simple customer support workflow with
personalisation and escalation logic layered on top of the core pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from context_engineering import ModelFamily, UCEF


@dataclass
class CustomerProfile:
    name: str
    tier: str  # e.g. "standard", "premium"
    preferred_tone: str


class DummySupportLLM:
    def __call__(self, prompt: str) -> str:
        return (
            "Hello {{name}},\n\n"
            "I am sorry to hear about the issue with your order. "
            "I have requested a full refund and sent a confirmation email.\n\n"
            "Best regards,\nSupport Bot"
        )


def personalise_output(output: str, profile: CustomerProfile) -> str:
    return output.replace("{{name}}", profile.name)


def needs_escalation(validation_score: float, profile: CustomerProfile) -> bool:
    if profile.tier == "premium":
        return validation_score < 0.85
    return validation_score < 0.7


def main() -> None:
    ucef = UCEF.default()
    llm: Any = DummySupportLLM()

    profile = CustomerProfile(name="Alex", tier="premium", preferred_tone="empathetic")

    user_input = "My order arrived damaged and I would like a refund."

    metadata: Dict[str, Any] = {
        "domain": "ecommerce",
        "complexity_level": "low",
        "quality_threshold": 0.8,
        "tone": profile.preferred_tone,
    }

    result = ucef.run_pipeline(
        user_input=user_input,
        model_family=ModelFamily.GPT4O,
        metadata=metadata,
        llm_callable=llm,
    )

    personalised = personalise_output(result["output"], profile)

    print("# Customer Response\n")
    print(personalised)

    print("\n# Validation\n")
    print(result["validation"])

    if needs_escalation(result["validation"].overall_score, profile):
        print("\n# Escalation\n")
        print("Route this conversation to a human agent with priority flag set.")


if __name__ == "__main__":
    main()
