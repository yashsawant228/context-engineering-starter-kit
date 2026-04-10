"""
Research analysis example.

Shows how to apply UCEF to a research synthesis task, including a hint for
citation accuracy checking. This is a scaffold; plug in your own retrieval and
evaluation layers.
"""

from __future__ import annotations

from typing import Any, Dict, List

from context_engineering import ModelFamily, UCEF


class DummyResearchLLM:
    def __call__(self, prompt: str) -> str:
        return (
            "## Summary\n\n"
            "Recent studies suggest that prompt engineering benefits from lifecycle-based "
            "frameworks rather than ad hoc experimentation [INFERRED].\n\n"
            "## Key Points\n"
            "- Treat prompts and configs as versioned artefacts.\n"
            "- Integrate evaluation harnesses into CI where possible.\n"
        )


class DummyRetriever:
    def retrieve(self, query: str, k: int) -> List[str]:
        return [
            "Paper A: Promptware engineering proposes treating prompts as software artefacts.",
            "Paper B: Surveys show a taxonomy of prompting techniques and best practices.",
        ]


def simple_citation_check(text: str, context_docs: List[str]) -> bool:
    if not context_docs:
        return False
    return "Promptware engineering" in " ".join(context_docs) and "Promptware" in text


def main() -> None:
    ucef = UCEF.default()
    # Inject a simple retriever
    ucef.context_retrieval.retriever = DummyRetriever()

    llm: Any = DummyResearchLLM()

    user_input = "Summarise recent research on prompt engineering methodologies and lifecycle frameworks."
    metadata: Dict[str, Any] = {
        "domain": "research",
        "complexity_level": "high",
        "quality_threshold": 0.85,
        "output_format": "Markdown summary with sections.",
    }

    result = ucef.run_pipeline(
        user_input=user_input,
        model_family=ModelFamily.GPT4O,
        metadata=metadata,
        llm_callable=llm,
    )

    enriched_context = ucef.context_retrieval.process(
        ucef.input_analysis.process(user_input, metadata)
    )
    context_docs = enriched_context.get("context", [])

    citation_ok = simple_citation_check(result["output"], context_docs)

    print("# Research Summary\n")
    print(result["output"])

    print("\n# Validation\n")
    print(result["validation"])
    print(f"\n# Citation Accuracy Check\nPass: {citation_ok}")


if __name__ == "__main__":
    main()
