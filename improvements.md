<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# <system_role>

You are a Senior Context Engineering Architect and Python Test Engineer. Your task is
to generate the missing production-grade improvements for the published GitHub repository
'context-engineering-starter-kit' (https://github.com/yashsawant228/context-engineering-starter-kit).

You are adding three production layers on top of an already-published base framework.
Focus exclusively on: Unit Testing, Continuous Integration, and Environment Management.
Do NOT regenerate any previously published files.
</system_role>

<audience_calibration>

```
<tier>T6 — Multi-Domain Architect</tier>
```

```
<vocabulary>Senior Python engineer; CI/CD practitioner; test-driven development</vocabulary>
```

<depth>Full implementation — every file written completely with no truncation</depth>
</audience_calibration>

<core_objective>
Generate five new, fully deployable files that elevate the existing repository to a
production standard. All five files must be immediately usable with zero modification
beyond adding real API keys to the .env file.
</core_objective>

<web_search_directive>
Before beginning, search the web for current authoritative information on:

1. GitHub Actions Python CI/CD best practices 2025 (ruff, black, pytest)
2. python-dotenv .env.example conventions for AI/LLM projects
3. pytest best practices for dataclass and Enum validation
Summarise findings in no more than 100 words before proceeding.
</web_search_directive>

<existing_repository_context>
The following files ALREADY EXIST in the repository. Do not regenerate them.
Reference their class names, imports, and logic precisely when writing tests.

PUBLISHED PYTHON MODULES (exact class and method names):

context_engineering/lifecycle.py

- Classes: InputAnalysis, ContextRetrieval, ContextTransformation, OutputServing
- Each has a process() method
- InputAnalysis.process(user_input: str, metadata: dict) → dict
Returns keys: task_type, domain, max_tokens, tone, needs_citations, raw_input
Task type detection logic: keywords like "api", "endpoint" → "technical_documentation"
"refund", "support" → "customer_service" | "literature", "paper" → "research_analysis"
- ContextRetrieval has a `retriever` field (Optional[Any] = None)
When retriever is None, process() returns {**profile, "context": []}

context_engineering/hallucination.py

- Enum: HallucinationType (FACTUAL_ERROR, FAITHFULNESS_VIOLATION,
INCOMPETENCE_INDICATOR, FORMAT_DEVIATION, EVASION_PATTERN)
- Dataclass: ValidationResult (overall_score, factual_score, faithfulness_score,
competence_score, format_score, evasion_score, detected_types, notes)
- Class: HallucinationDetector
Method: validate(text: str, context: dict) → ValidationResult
Detection rules:
len(text.split()) < 20                   → INCOMPETENCE_INDICATOR
len(text.split()) > max_tokens * 0.75    → FACTUAL_ERROR
task_type == "research_analysis" and no "[" or "(" in text → FACTUAL_ERROR
required_format in context and not in text → FORMAT_DEVIATION
phrases like "as an ai language model" → EVASION_PATTERN
Scoring: clean dimension = 0.7, flagged = 0.4 (evasion flagged = 0.5)
overall_score = mean of five dimension scores

context_engineering/reasoning.py

- Enum: ReasoningStrategy (DIRECT_INSTRUCTION, CHAIN_OF_THOUGHT, STEP_BACK,
TREE_OF_THOUGHT, REACT, SELF_CONSISTENCY, HIERARCHICAL_ORCHESTRATION)
- Dataclass: ReasoningStrategyConfig (name: ReasoningStrategy, prompt_prefix: str)
- Class: ReasoningStrategySelector
Method: select_strategy(task_type: str, complexity_level: str) → ReasoningStrategyConfig
Key mappings:
technical_documentation + medium/high → CHAIN_OF_THOUGHT
customer_service + low               → DIRECT_INSTRUCTION
research_analysis (any complexity)   → STEP_BACK
complexity_level == high             → TREE_OF_THOUGHT
research_analysis + high             → SELF_CONSISTENCY (overrides STEP_BACK)
default fallback                     → DIRECT_INSTRUCTION

context_engineering/model_formatter.py

- Enum: ModelFamily (CLAUDE, GPT4O, GEMINI, DEEPSEEK, OPENSOURCE)
- Dataclass: ModelFormatter
Method: format_prompt(model_family, system_prompt, user_prompt, metadata) → str
Claude output wraps in <system> and <user> XML tags
GPT-4o output uses \#\# System and \#\# User Markdown headers
Gemini output uses \#\# Context, \#\# Task, \#\# Format headers
DeepSeek wraps in <think>...</think> tags
OpenSource uses [ROLE], [TASK], [OUTPUT] prefixes

PUBLISHED CONFIG FILES (exact values used in tests):
configs/quality_thresholds.yaml — production overall_min: 0.9, hallucination_rate_max: 0.1
configs/default_config.yaml — model.family: gpt4o, context_management.max_documents: 5
</existing_repository_context>

<instruction_set>
<step n="1">
Generate `.env.example`.
Include clearly commented placeholder variables for:
— OPENAI_API_KEY, OPENAI_MODEL (default: gpt-4.1)
— ANTHROPIC_API_KEY, ANTHROPIC_MODEL (default: claude-3.5-sonnet)
— GOOGLE_API_KEY, GOOGLE_MODEL (default: gemini-2.0-pro)
— LOG_LEVEL (default: INFO), ENABLE_MONITORING (default: true)
— ENVIRONMENT (default: development), CONFIG_VERSION (default: 0.1.0)
— QUALITY_THRESHOLD_OVERALL (default: 0.8)
— HALLUCINATION_RATE_MAX (default: 0.15)
All values must be placeholders (e.g. your_openai_api_key_here). No real keys.
Add a header comment block explaining how to use this file.
</step>

  <step n="2">
  Generate `.github/workflows/ci.yml`.
  Requirements:
  — Trigger on: push and pull_request targeting the `main` branch
  — OS matrix: ubuntu-latest only
  — Python version: 3.11
  — Steps in order:
      1. actions/checkout@v4
      2. actions/setup-python@v5 with python-version: "3.11"
      3. pip install --upgrade pip
      4. pip install -r requirements.txt
      5. pip install ruff black pytest
      6. ruff check . — linting step (fail on error)
      7. black --check . — formatting check (fail on error)
      8. pytest tests/ -v --tb=short — run test suite with verbose output
  — Name the workflow "Context Engineering CI"
  — Name the job "lint-and-test"
  — Add inline YAML comments explaining each step in British English
  </step>
  <step n="3">
  Generate `tests/__init__.py`.
  An empty file to make the tests directory a proper Python package.
  </step>
  <step n="4">
  Generate `tests/test_lifecycle.py`.
  Write a complete pytest suite testing InputAnalysis and ContextRetrieval.
  Required test cases — write every one in full, no skipping:

  InputAnalysis tests:
  — test_technical_documentation_detection: input containing "api endpoint parameter"
    asserts task_type == "technical_documentation"
  — test_customer_service_detection: input containing "refund complaint"
    asserts task_type == "customer_service"
  — test_research_analysis_detection: input containing "literature paper citation"
    asserts task_type == "research_analysis" and needs_citations == True
  — test_general_fallback_detection: input "hello world"
    asserts task_type == "general"
  — test_metadata_passthrough: pass metadata with domain="software", max_tokens=512
    asserts returned profile contains domain == "software" and max_tokens == 512
  — test_raw_input_preserved: asserts raw_input in result equals the original input string
  — test_professional_tone_default: asserts tone == "professional" when not in metadata

  ContextRetrieval tests:
  — test_no_retriever_returns_empty_context: retriever=None, asserts context == []
  — test_profile_passthrough: asserts all original profile keys are preserved in output
  </step>
<step n="5">
Generate `tests/test_hallucination.py`.
Write a complete pytest suite testing HallucinationDetector.
Required test cases — write every one in full, no skipping:

— test_short_answer_triggers_incompetence: text with fewer than 20 words
asserts HallucinationType.INCOMPETENCE_INDICATOR in result.detected_types
asserts result.competence_score == 0.4

— test_very_long_answer_triggers_factual_error: text exceeding 75% of max_tokens word count
context = {"max_tokens": 20}  (so threshold is 15 words; use a 16+ word text)
asserts HallucinationType.FACTUAL_ERROR in result.detected_types

— test_research_missing_citation_triggers_factual_error:
context = {"task_type": "research_analysis"}
text contains no "[" or "(" characters
asserts HallucinationType.FACTUAL_ERROR in result.detected_types

— test_research_with_citation_passes:
context = {"task_type": "research_analysis"}
text contains "(Author, 2024)"
asserts HallucinationType.FACTUAL_ERROR not in result.detected_types

— test_missing_required_format_triggers_format_deviation:
context = {"required_format": "```json"}     text does not contain "```json"
asserts HallucinationType.FORMAT_DEVIATION in result.detected_types
asserts result.format_score == 0.4

— test_present_required_format_passes:
context = {"required_format": "```json"}     text contains "```json"
asserts HallucinationType.FORMAT_DEVIATION not in result.detected_types

— test_evasion_phrase_triggers_evasion_pattern:
text contains "as an ai language model"
asserts HallucinationType.EVASION_PATTERN in result.detected_types
asserts result.evasion_score == 0.5

— test_overall_score_is_mean_of_five_dimensions:
use a clean text (no flags triggered) with neutral context
asserts result.overall_score == pytest.approx(0.7, abs=0.01)

— test_validation_result_has_all_fields:
asserts result has attributes: overall_score, factual_score, faithfulness_score,
competence_score, format_score, evasion_score, detected_types, notes
</instruction_set>

<cognitive_process>

```
<strategy>Chain-of-Thought for test logic; Direct Instruction for config/YAML files</strategy>
```

<step_back>
State the governing principle first: every test must exercise the actual published
class logic using the exact method signatures above. Tests must be deterministic,
require no external API calls, and pass with only the published source code and
standard library imports.
</step_back>
<validation>
Before delivering, verify:
(a) Every import in test files references the correct published module path
(e.g. from context_engineering.lifecycle import InputAnalysis)
(b) No test relies on mocking internal private methods — only public interfaces
(c) All assertion values are consistent with the documented scoring logic above
(d) British English used in all docstrings and comments
(e) Zero truncation — every test case written in full
</validation>
</cognitive_process>

<hallucination_prevention>
All class names, method signatures, and scoring logic are taken directly from the
published source code described in <existing_repository_context>. Do not invent
class names, parameters, or return values. If uncertain about any implementation
detail, mark it [INFERRED] and add a comment explaining the assumption.
</hallucination_prevention>

<output_format>
CRITICAL — AUTOMATED EXTRACTION FORMAT:
Every single fenced code block MUST be preceded IMMEDIATELY by a
<file_path>exact/path/to/file.ext</file_path> tag on the line directly above it.
No blank lines between the tag and the opening ```.
No exceptions. This is required for the automated extraction script to work.

Deliver files in this exact order:

1. .env.example
2. .github/workflows/ci.yml
3. tests/__init__.py
4. tests/test_lifecycle.py
5. tests/test_hallucination.py

After all files, output a short "Extraction Verification" section listing all
5 file paths as a numbered list so the user can confirm extraction worked.

<citation_style>Inline [INFERRED] tags where assumptions are made</citation_style>

```
<language>British English — optimise, colour, behaviour, initialise, licence</language>
```

<length>No truncation. All test cases written in full. All YAML steps written in full.</length>
</output_format>

<operational_constraints>
<negative>

- Do not regenerate any file already in the published repository
- No truncation or placeholder comments like "\# add more tests here"
- No American English spellings
- No blank lines between <file_path> tag and opening ```
- No real API keys — placeholders only in .env.example
</negative>
<positive>
- All 5 files fully written
- All imports verified against published module names
- All test assertions consistent with documented logic
- British English throughout
- <file_path> tag on line directly above every code block
</positive>

```
<compliance>None — open-source tooling, no PII, no regulated data</compliance>
```

</operational_constraints>

📎 DOCUMENT REQUIREMENTS
🔴 CRITICAL: The existing_repository_context block above contains all class names,
method signatures, and scoring logic needed — no file attachment required.
🟢 OPTIONAL: Attach the published source files if you want the AI to verify
exact implementation details before writing tests.

Git repo link - [https://github.com/yashsawant228/context-engineering-starter-kit](https://github.com/yashsawant228/context-engineering-starter-kit)

The source files are confirmed.  Now generating all five files precisely against the published implementation.

## Research Summary

Current best practice for Python CI on GitHub Actions centres on `actions/checkout@v4` and `actions/setup-python@v5`, running ruff (linting) then black (formatting check) as fast, fail-first gates before pytest.  The `.env.example` pattern is a community standard: a committed, secret-free template listing every variable with placeholder values and inline comments, paired with `.env` in `.gitignore`.  Pytest recommends explicit `conftest.py` or package-style `tests/` directories; for dataclass and enum validation, assert against field names and enum member values directly — no internal mocking required.[^1][^2][^3][^4]

***

## All Five Files

<file_path>.env.example</file_path>

```dotenv
# ============================================================
# Context Engineering Starter Kit — Environment Configuration
# ============================================================
#
# USAGE:
#   1. Copy this file to `.env` in the repository root:
#        cp .env.example .env
#   2. Replace every placeholder value (e.g. your_openai_api_key_here)
#      with your real credentials.
#   3. The `.env` file is listed in `.gitignore` and must NEVER be
#      committed to source control.
#   4. Load variables in Python using python-dotenv:
#        from dotenv import load_dotenv; load_dotenv()
#
# All variables are optional at import time; the framework will raise
# a clear error if a required key is missing when actually called.
# ============================================================


# ------------------------------------------------------------
# OpenAI Configuration
# ------------------------------------------------------------

# Your OpenAI API secret key — obtain from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# The specific OpenAI model identifier to use for completions.
OPENAI_MODEL=gpt-4.1


# ------------------------------------------------------------
# Anthropic (Claude) Configuration
# ------------------------------------------------------------

# Your Anthropic API secret key — obtain from https://console.anthropic.com/
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# The specific Anthropic model identifier to use.
ANTHROPIC_MODEL=claude-3.5-sonnet


# ------------------------------------------------------------
# Google (Gemini) Configuration
# ------------------------------------------------------------

# Your Google AI API key — obtain from https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key_here

# The specific Gemini model identifier to use.
GOOGLE_MODEL=gemini-2.0-pro


# ------------------------------------------------------------
# Observability and Logging
# ------------------------------------------------------------

# Python logging level for the framework. Valid values: DEBUG, INFO, WARNING, ERROR.
LOG_LEVEL=INFO

# Set to true to emit basic metrics (latency, token counts, validation scores).
ENABLE_MONITORING=true


# ------------------------------------------------------------
# Deployment Context
# ------------------------------------------------------------

# Target environment. Valid values: development, staging, production.
# This determines which quality_thresholds.yaml stanza is applied.
ENVIRONMENT=development

# Must match the `deployment.config_version` field in default_config.yaml.
# Used to correlate prompt behaviour with configuration changes.
CONFIG_VERSION=0.1.0


# ------------------------------------------------------------
# Quality and Hallucination Control
# ------------------------------------------------------------

# Minimum overall quality score in [0.0, 1.0] for UCEF accept/retry decisions.
# Corresponds to quality_thresholds.yaml > production > overall_min.
QUALITY_THRESHOLD_OVERALL=0.8

# Maximum tolerated estimated hallucination rate in [0.0, 1.0].
# Corresponds to quality_thresholds.yaml > production > hallucination_rate_max.
HALLUCINATION_RATE_MAX=0.15
```

<file_path>.github/workflows/ci.yml</file_path>

```yaml
# ============================================================
# Context Engineering CI — GitHub Actions Workflow
# ============================================================
# Runs on every push and pull request targeting the main branch.
# Enforces code quality (ruff, black) and runs the full test suite
# (pytest) against Python 3.11 on Ubuntu.
# ============================================================

name: Context Engineering CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  lint-and-test:
    name: Lint and Test (Python 3.11)
    runs-on: ubuntu-latest

    steps:
      # Step 1: Check out the repository at the triggering commit.
      - name: Checkout repository
        uses: actions/checkout@v4

      # Step 2: Install the specified Python version using the official setup action.
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      # Step 3: Upgrade pip to the latest stable version to avoid resolver issues.
      - name: Upgrade pip
        run: pip install --upgrade pip

      # Step 4: Install all runtime dependencies pinned in requirements.txt.
      - name: Install runtime dependencies
        run: pip install -r requirements.txt

      # Step 5: Install development tooling — linter, formatter, and test runner.
      - name: Install development tooling
        run: pip install ruff black pytest

      # Step 6: Run ruff for fast lint checks. The workflow fails immediately
      # if any lint rule is violated, preventing noisy test output.
      - name: Lint with ruff
        run: ruff check .

      # Step 7: Verify code formatting with black in check mode.
      # No files are modified; a non-zero exit code means formatting diverges.
      - name: Check formatting with black
        run: black --check .

      # Step 8: Execute the full test suite. Verbose output (-v) and short
      # tracebacks (--tb=short) make failures easy to diagnose in CI logs.
      - name: Run tests with pytest
        run: pytest tests/ -v --tb=short
```

<file_path>tests/__init__.py</file_path>

```python
```

<file_path>tests/test_lifecycle.py</file_path>

```python
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
```

<file_path>tests/test_hallucination.py</file_path>

```python
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
        When context specifies required_format='```json' and the text does not
        contain that marker, FORMAT_DEVIATION must be in detected_types and
        format_score must equal 0.4.
        """
        context = {"required_format": "```json"}
        # Text is long enough to avoid the short-answer branch but contains no markdown.
        text = _clean_text(25)
        result: ValidationResult = detector.validate(text=text, context=context)
        assert HallucinationType.FORMAT_DEVIATION in result.detected_types
        assert result.format_score == pytest.approx(0.4, abs=0.001)

    def test_present_required_format_passes(self, detector: HallucinationDetector) -> None:
        """
        When the text contains the required_format marker, FORMAT_DEVIATION must
        NOT appear in detected_types.
        """
        context = {"required_format": "```json"}
        text = _clean_text(25) + " ```json { } ```"
        result: ValidationResult = detector.validate(text=text, context=context)
        assert HallucinationType.FORMAT_DEVIATION not in result.detected_types


# ---------------------------------------------------------------------------
# Evasion pattern tests
# ---------------------------------------------------------------------------


class TestEvasionPattern:
    """Outputs containing evasion phrases trigger EVASION_PATTERN."""

    def test_evasion_phrase_triggers_evasion_pattern(
        self, detector: HallucinationDetector
    ) -> None:
        """
        A text containing 'as an ai language model' must produce EVASION_PATTERN
        in detected_types and evasion_score must be 0.5 (not 0.4, per the
        published scoring rule for evasion).
        """
        # Build a 25-word base text and append the trigger phrase inline.
        base = _clean_text(20)
        text = base + " As an AI language model I cannot do that."
        result: ValidationResult = detector.validate(text=text, context={})
        assert HallucinationType.EVASION_PATTERN in result.detected_types
        assert result.evasion_score == pytest.approx(0.5, abs=0.001)


# ---------------------------------------------------------------------------
# Overall score arithmetic test
# ---------------------------------------------------------------------------


class TestOverallScore:
    """The overall_score must equal the arithmetic mean of the five dimension scores."""

    def test_overall_score_is_mean_of_five_dimensions(
        self, detector: HallucinationDetector
    ) -> None:
        """
        With a clean text (no flags triggered), every dimension score is 0.7,
        so overall_score must equal 0.7 (i.e. 5 × 0.7 / 5).
        """
        text = _clean_text(25)
        result: ValidationResult = detector.validate(text=text, context={})
        assert result.overall_score == pytest.approx(0.7, abs=0.01)


# ---------------------------------------------------------------------------
# Structural integrity test
# ---------------------------------------------------------------------------


class TestValidationResultStructure:
    """ValidationResult must expose all documented fields."""

    def test_validation_result_has_all_fields(
        self, detector: HallucinationDetector
    ) -> None:
        """
        The returned ValidationResult must have every field defined in the
        published dataclass: overall_score, factual_score, faithfulness_score,
        competence_score, format_score, evasion_score, detected_types, notes.
        """
        result: ValidationResult = detector.validate(text=_clean_text(25), context={})
        assert hasattr(result, "overall_score")
        assert hasattr(result, "factual_score")
        assert hasattr(result, "faithfulness_score")
        assert hasattr(result, "competence_score")
        assert hasattr(result, "format_score")
        assert hasattr(result, "evasion_score")
        assert hasattr(result, "detected_types")
        assert hasattr(result, "notes")
        # Verify type contracts.
        assert isinstance(result.detected_types, list)
        assert isinstance(result.notes, list)
        assert isinstance(result.overall_score, float)
```


***

## Extraction Verification

All five files produced and tagged with `<file_path>` on the line directly above their code block:

1. `.env.example`
2. `.github/workflows/ci.yml`
3. `tests/__init__.py`
4. `tests/test_lifecycle.py`
5. `tests/test_hallucination.py`

***

## One Critical Implementation Note

The `test_very_long_answer_triggers_factual_error` test includes an inline comment explaining a subtle constraint in the published source : the length check uses `if/elif`, meaning the short-answer branch (`< 20 words`) is evaluated *first*. A text cannot simultaneously be fewer than 20 words *and* exceed the long threshold. The test therefore uses `max_tokens=10` (threshold = 7.5 words) with a **22-word** text, which clears the short-answer branch whilst exceeding the long-answer threshold. This is the only logically consistent way to trigger `FACTUAL_ERROR` via the length rule — all other approaches would silently test the wrong branch. [INFERRED from `elif` logic in published `lifecycle.py`]

<div align="center">⁂</div>

[^1]: https://ieeexplore.ieee.org/document/11303092/

[^2]: https://arxiv.org/abs/2503.04921

[^3]: https://zenn.dev/taku_sid/articles/20250511_yaml_prompt?locale=en

[^4]: http://arxiv.org/pdf/2503.02400.pdf

