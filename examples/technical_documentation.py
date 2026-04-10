"""
Technical documentation example using UCEF.

This script demonstrates how to apply the UCEF pipeline to an API documentation
task. It is structured so that teams can reproduce improvements in accuracy and
time-to-draft compared with purely manual authoring [INFERRED].
"""

from __future__ import annotations

import os
from typing import Any

from context_engineering import ModelFamily, UCEF


class DummyLLM:
    """
    Minimal stand-in for a real LLM client.

    Replace the `__call__` implementation with calls to your provider
    (e.g. OpenAI, Anthropic, Gemini) using the prompt string.
    """

    def __call__(self, prompt: str) -> str:
        # In a real system, you would send `prompt` to your LLM API here.
        # This placeholder returns a short, deterministic response for testing.
        return (
            "## Authentication Flow\n\n"
            "1. The client requests an access token using client credentials.\n"
            "2. The server validates the credentials and issues a time-limited token.\n"
            "3. The client includes the token in the `Authorization` header on each request.\n"
            "4. If the token expires or is invalid, the API returns `401 Unauthorized`.\n"
        )


def main() -> None:
    # Instantiate UCEF with defaults.
    ucef = UCEF.default()
    llm: Any = DummyLLM()

    user_input = "Document the authentication flow for our payment API, including error handling."
    metadata = {
        "domain": "payments",
        "complexity_level": "medium",
        "quality_threshold": 0.8,
        "output_format": "Markdown with headings and numbered steps.",
    }

    result = ucef.run_pipeline(
        user_input=user_input,
        model_family=ModelFamily.GPT4O,
        metadata=metadata,
        llm_callable=llm,
    )

    print("# Generated Documentation\n")
    print(result["output"])
    print("\n# Validation\n")
    print(result["validation"])


if __name__ == "__main__":
    main()
