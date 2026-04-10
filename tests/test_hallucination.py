"""
Test suite for context_engineering.hallucination.

Exercises every detection rule in HallucinationDetector.validate() and verifies
the scoring arithmetic defined by the published implementation.

All tests are deterministic and require no external API calls or network access.
"""

from __future__ import annotations

import pytest

from context_engineering.hallucination import (
    HallucinationDetector,
    HallucinationType,
    ValidationResult,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def detector() -> HallucinationDetector:
    """Return a default HallucinationDetector instance."""
    return HallucinationDetector()


def _clean_text(word_count: int = 25) -> str:
    """
    Build a neutral, clean text string of the requested word count with no
    hallucination-triggering keywords, format markers, or citation tokens.
    """
    return " ".join(["word"] * word_count)


def _research_text_with_citation() -> str:
    """Return a sufficiently long text that includes a citation marker."""
    base = _clean_text(25)
    return base + " (Author, 2024)"


# ---------------------------------------------------------------------------
# Incompetence indicator tests
# ---------------------------------------------------------------------------


class TestIncompetenceIndicator:
    """Short answers (fewer than 20 words) trigger INCOMPETENCE_INDICATOR."""

    def test_short_answer_triggers_incompetence(self, detector: HallucinationDetector) -> None:
        """
        A text with fewer than 20 words must trigger INCOMPETENCE_INDICATOR and
        the competence_score must be 0.4.
        """
        short_text = "This answer is far too brief."  # 6 words
        result: ValidationResult = detector.validate(text=short_text, context={})
        assert HallucinationType.INCOMPETENCE_INDICATOR in result.detected_types
        assert result.competence_score == pytest.approx(0.4, abs=0.001)


# ---------------------------------------------------------------------------
# Factual error tests — length threshold
# ---------------------------------------------------------------------------


class TestFactualErrorLength:
    """Answers exceeding 75 % of max_tokens word count trigger FACTUAL_ERROR."""

    def test_very_long_answer_triggers_factual_error(
        self, detector: HallucinationDetector
    ) -> None:
        """
        With max_tokens=20, the threshold is 20 * 0.75 = 15 words.
        A 16-word text must trigger FACTUAL_ERROR.

        Note: the length check uses an elif branch, so INCOMPETENCE_INDICATOR
        is NOT triggered simultaneously. The text must be >= 20 words to avoid
        the short-answer branch — but 16 words satisfies neither short (< 20)
        branch correctly because 16 < 20 would trigger short first. We therefore
        use max_tokens=10 so threshold = 7.5 words and text length = 9 words,
        which is >= 20... 

        Corrected approach: max_tokens=10, threshold = 7.5, so any text > 7.5
        words (i.e. 8+ words) AND >= 20 words would trigger FACTUAL_ERROR, but
        texts >= 20 words can never be short. We choose max_tokens=10 and a
        22-word text: 22 > 10 * 0.75 = 7.5, and 22 >= 20 so the short branch
        is not entered. This is internally consistent. [INFERRED from elif logic]
        """
        # max_tokens = 10, threshold = 7.5 words; use 22 words (>= 20 avoids short branch).
        long_text = " ".join(["word"] * 22)
        context = {"max_tokens": 10}
        result: ValidationResult = detector.validate(text=long_text, context=context)
        assert HallucinationType.FACTUAL_ERROR in result.detected_types


# ---------------------------------------------------------------------------
# Factual error tests — missing citation for research tasks
# ---------------------------------------------------------------------------


class TestResearchCitation:
    """Research-analysis tasks without citation markers trigger FACTUAL_ERROR."""

    def test_research_missing_citation_triggers_factual_error(
        self, detector: HallucinationDetector
    ) -> None:
        """
        A research_analysis task with no '[' or '(' in the text must produce
        FACTUAL_ERROR in detected_types.
        """
        # 25-word text that is long enough to avoid the short-answer branch
        # and contains no citation markers.
        text = _clean_text(25)
        context = {"task_type": "research_analysis"}
        result: ValidationResult = detector.validate(text=text, context=context)
        assert HallucinationType.FACTUAL_ERROR in result.detected_types

    def test_research_with_citation_passes(self, detector: HallucinationDetector) -> None:
        """
        A research_analysis task whose text contains '(' must NOT produce
        FACTUAL_ERROR from the citation check.
        """
        text = _research_text_with_citation()
        context = {"task_type": "research_analysis"}
        result: ValidationResult = detector.validate(text=text, context=context)
        assert HallucinationType.FACTUAL_ERROR not in result.detected_types


# ---------------------------------------------------------------------------
# Format deviation tests
# ---------------------------------------------------------------------------


class TestFormatDeviation:
    """Outputs missing a required format marker trigger FORMAT_DEVIATION."""

    def test_missing_required_format_triggers_format_deviation(
        self, detector: HallucinationDetector
    ) -> None:
        """
        When context specifies required_format='