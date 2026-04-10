from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class HallucinationType(str, Enum):
    """
    Five hallucination types adapted from the guidebook taxonomy.

    - FACTUAL_ERROR: Contradicts verifiable facts or ground truth.
    - FAITHFULNESS_VIOLATION: Misrepresents or fabricates from the provided context.
    - INCOMPETENCE_INDICATOR: Obvious mistakes (nonsense maths, impossible claims).
    - FORMAT_DEVIATION: Ignoring required structure or output schema.
    - EVASION_PATTERN: Overconfident answers where uncertainty should be signalled.
    """

    FACTUAL_ERROR = "factual_error"
    FAITHFULNESS_VIOLATION = "faithfulness_violation"
    INCOMPETENCE_INDICATOR = "incompetence_indicator"
    FORMAT_DEVIATION = "format_deviation"
    EVASION_PATTERN = "evasion_pattern"


@dataclass
class ValidationResult:
    """
    Structured result of hallucination and quality checks.

    The scores are in [0.0, 1.0], where higher is better quality (lower
    hallucination likelihood).
    """

    overall_score: float
    factual_score: float
    faithfulness_score: float
    competence_score: float
    format_score: float
    evasion_score: float
    detected_types: List[HallucinationType]
    notes: List[str]


class HallucinationDetector:
    """
    Heuristic hallucination detector.

    This starter implementation uses simple heuristics and metadata to estimate
    confidence; in production you may plug in a dedicated uncertainty
    quantification or evaluator model, as suggested in recent practitioner work.[web:35]
    """

    def validate(self, text: str, context: Dict[str, Any]) -> ValidationResult:
        """
        Analyse the output text and return a ValidationResult.

        The heuristics here are intentionally conservative and easily replaceable:
        - Penalise extremely short or extremely long answers.
        - Penalise absence of citations for research tasks.
        - Penalise responses that ignore obvious format markers.
        """
        notes: List[str] = []
        detected: List[HallucinationType] = []

        length = len(text.split())
        if length < 20:
            notes.append("Answer is very short; may lack necessary detail.")
            detected.append(HallucinationType.INCOMPETENCE_INDICATOR)
        elif length > context.get("max_tokens", 2048) * 0.75:
            notes.append("Answer is very long; may contain off-topic content.")
            detected.append(HallucinationType.FACTUAL_ERROR)

        if context.get("task_type") == "research_analysis":
            if "[" not in text and "(" not in text:
                notes.append("No visible citations for research task.")
                detected.append(HallucinationType.FACTUAL_ERROR)

        required_format = context.get("required_format")
        if required_format and required_format not in text:
            notes.append(f"Required format marker '{required_format}' not present in output.")
            detected.append(HallucinationType.FORMAT_DEVIATION)

        if any(
            phrase in text.lower()
            for phrase in ["as an ai language model", "cannot access the internet"]
        ):
            notes.append("Model surfaced internal limitations; treat with caution.")
            detected.append(HallucinationType.EVASION_PATTERN)

        # Assign simple scores; production systems should use calibrated metrics.
        factual_score = 0.7 if HallucinationType.FACTUAL_ERROR not in detected else 0.4
        faithfulness_score = (
            0.7 if HallucinationType.FAITHFULNESS_VIOLATION not in detected else 0.4
        )
        competence_score = (
            0.7 if HallucinationType.INCOMPETENCE_INDICATOR not in detected else 0.4
        )
        format_score = 0.7 if HallucinationType.FORMAT_DEVIATION not in detected else 0.4
        evasion_score = 0.7 if HallucinationType.EVASION_PATTERN not in detected else 0.5

        overall_score = (
            factual_score + faithfulness_score + competence_score + format_score + evasion_score
        ) / 5.0

        return ValidationResult(
            overall_score=overall_score,
            factual_score=factual_score,
            faithfulness_score=faithfulness_score,
            competence_score=competence_score,
            format_score=format_score,
            evasion_score=evasion_score,
            detected_types=list(set(detected)),
            notes=notes,
        )
