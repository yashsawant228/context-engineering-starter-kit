"""
Test suite for context_engineering.lifecycle.

Covers InputAnalysis task-type detection, metadata passthrough, and
ContextRetrieval behaviour in the absence of a retriever.

All tests are deterministic and require no external API calls or network access.
"""

from __future__ import annotations

import pytest

from context_engineering.lifecycle import ContextRetrieval, InputAnalysis


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def analyser() -> InputAnalysis:
    """Return a default InputAnalysis instance."""
    return InputAnalysis()


@pytest.fixture()
def retrieval_no_retriever() -> ContextRetrieval:
    """Return a ContextRetrieval instance with no retriever attached."""
    return ContextRetrieval(retriever=None)


# ---------------------------------------------------------------------------
# InputAnalysis tests
# ---------------------------------------------------------------------------


class TestInputAnalysis:
    """Tests for InputAnalysis.process() covering all task-type branches."""

    def test_technical_documentation_detection(self, analyser: InputAnalysis) -> None:
        """
        Inputs containing technical keywords ('api', 'endpoint', 'parameter')
        should produce task_type == 'technical_documentation'.
        """
        result = analyser.process("Document the api endpoint parameter schema.")
        assert result["task_type"] == "technical_documentation"

    def test_customer_service_detection(self, analyser: InputAnalysis) -> None:
        """
        Inputs containing service keywords ('refund', 'complaint') should
        produce task_type == 'customer_service'.
        """
        result = analyser.process("I want a refund for my complaint about the product.")
        assert result["task_type"] == "customer_service"

    def test_research_analysis_detection(self, analyser: InputAnalysis) -> None:
        """
        Inputs containing research keywords ('literature', 'paper', 'citation')
        should produce task_type == 'research_analysis' and needs_citations == True.
        """
        result = analyser.process("Summarise recent literature on paper citation practices.")
        assert result["task_type"] == "research_analysis"
        assert result["needs_citations"] is True

    def test_general_fallback_detection(self, analyser: InputAnalysis) -> None:
        """
        Inputs with no domain-specific keywords should fall back to
        task_type == 'general'.
        """
        result = analyser.process("hello world")
        assert result["task_type"] == "general"

    def test_metadata_passthrough(self, analyser: InputAnalysis) -> None:
        """
        Values provided in the metadata dict (domain, max_tokens) should
        appear verbatim in the returned profile dictionary.
        """
        metadata = {"domain": "software", "max_tokens": 512}
        result = analyser.process("hello world", metadata=metadata)
        assert result["domain"] == "software"
        assert result["max_tokens"] == 512

    def test_raw_input_preserved(self, analyser: InputAnalysis) -> None:
        """
        The original user input string must be stored unchanged under the
        'raw_input' key of the returned profile.
        """
        user_input = "A distinctly specific input string for traceability."
        result = analyser.process(user_input)
        assert result["raw_input"] == user_input

    def test_professional_tone_default(self, analyser: InputAnalysis) -> None:
        """
        When the 'tone' key is absent from metadata, the profile should
        default to 'professional'.
        """
        result = analyser.process("hello world", metadata={})
        assert result["tone"] == "professional"


# ---------------------------------------------------------------------------
# ContextRetrieval tests
# ---------------------------------------------------------------------------


class TestContextRetrieval:
    """Tests for ContextRetrieval.process() with no retriever configured."""

    def test_no_retriever_returns_empty_context(
        self, retrieval_no_retriever: ContextRetrieval
    ) -> None:
        """
        When retriever is None, process() must return a dict containing
        'context' as an empty list.
        """
        profile = {
            "task_type": "general",
            "domain": "general",
            "max_tokens": 1024,
            "tone": "professional",
            "needs_citations": False,
            "raw_input": "hello world",
        }
        result = retrieval_no_retriever.process(profile)
        assert result["context"] == []

    def test_profile_passthrough(self, retrieval_no_retriever: ContextRetrieval) -> None:
        """
        All keys present in the original profile must still be present in
        the output, with their values unchanged.
        """
        profile = {
            "task_type": "technical_documentation",
            "domain": "payments",
            "max_tokens": 512,
            "tone": "professional",
            "needs_citations": False,
            "raw_input": "Document the payment api endpoint.",
        }
        result = retrieval_no_retriever.process(profile)
        for key, value in profile.items():
            assert result[key] == value, (
                f"Expected profile key '{key}' to be '{value}', got '{result[key]}'"
            )
