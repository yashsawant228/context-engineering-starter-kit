# Hallucination Prevention

This document summarises the five hallucination types from the guidebook and describes the defence mechanisms implemented in this starter kit.

## Hallucination Types

1. **Factual Errors** — Statements that contradict verifiable facts or ground truth.
2. **Faithfulness Violations** — Misrepresentations of the provided context or invented citations.
3. **Incompetence Indicators** — Obvious mistakes such as impossible numbers or broken logic.
4. **Format Deviations** — Outputs that ignore required schemas, headings, or JSON structures.
5. **Evasion Patterns** — Overconfident or evasive responses that mask uncertainty.

## Defence Mechanisms

- **Lifecycle Design** — Retrieval and transformation stages encourage grounded answers by foregrounding high-signal context.
- **Reasoning Control** — Step-back and self-consistency strategies encourage more cautious, reflective answers for complex tasks.[web:22]
- **Heuristic Detector** — `HallucinationDetector` flags likely issues and assigns simple scores.
- **Iterative Refinement** — UCEF optionally triggers one retry when quality scores are too low.
- **Observability Hooks** — Configuration options allow attaching detector notes to responses for monitoring.

## Confidence Tagging

For research and analysis tasks, encourage the model to label its answers with a confidence tag:

- **HIGH** — Strong support in context or widely accepted sources.
- **MEDIUM** — Reasonable support but some gaps or assumptions.
- **LOW** — Significant uncertainty or missing context.
- **INFERRED** — Based primarily on extrapolation rather than explicit sources.

Combine these tags with human or automated review in higher-risk settings.
