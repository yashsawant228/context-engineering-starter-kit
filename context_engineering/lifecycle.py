from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class InputAnalysis:
    """
    InputAnalysis implements the Generation (input analysis) stage of the
    four-stage context engineering lifecycle described in the guidebook.

    It inspects raw user input and upstream metadata to derive:
    - task type (e.g. documentation, support, research)
    - domain (e.g. software, legal, health)
    - constraints (length, style, safety)
    - context requirements (retrieval depth, freshness, modality needs)
    """

    def process(self, user_input: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyse the incoming request and derive a structured task profile.

        The implementation here is intentionally lightweight; in production you
        would replace this with a classifier or rules tailored to your domain.
        """
        metadata = metadata or {}
        lower = user_input.lower()

        if any(kw in lower for kw in ["api", "endpoint", "parameter", "sdk"]):
            task_type = "technical_documentation"
        elif any(kw in lower for kw in ["refund", "support", "complaint", "order"]):
            task_type = "customer_service"
        elif any(kw in lower for kw in ["literature", "paper", "citation", "reference"]):
            task_type = "research_analysis"
        else:
            task_type = "general"

        profile = {
            "task_type": task_type,
            "domain": metadata.get("domain", "general"),
            "max_tokens": metadata.get("max_tokens", 1024),
            "tone": metadata.get("tone", "professional"),
            "needs_citations": task_type == "research_analysis",
            "raw_input": user_input,
        }
        return profile


@dataclass
class ContextRetrieval:
    """
    ContextRetrieval implements the Storage/Retrieval stage of the lifecycle.

    It takes a task profile and retrieves high-signal context from available
    sources (e.g. vector stores, document indices, configuration registries).
    This starter kit uses a pluggable callback for retrieval to keep the core
    implementation simple.
    """

    retriever: Optional[Any] = None

    def process(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve contextual documents based on the task profile.

        The `retriever` is expected to expose a `retrieve(query: str, k: int)` method
        returning a list of strings or document-like objects. In tests and simple
        examples, `retriever` may be None, in which case an empty context list
        is returned.
        """
        if self.retriever is None:
            return {**profile, "context": []}

        query = profile.get("raw_input", "")
        k = 5
        docs: List[Any] = self.retriever.retrieve(query=query, k=k)  # type: ignore[call-arg]
        return {**profile, "context": docs}


@dataclass
class ContextTransformation:
    """
    ContextTransformation implements the Transformation (prompt construction)
    stage of the lifecycle.

    It takes the analysed input and retrieved context and constructs a
    model-ready prompt payload, delegating model-specific formatting to an
    injected formatter.
    """

    formatter: Any

    def process(self, enriched: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a structured prompt for the target model family.

        The enriched dictionary is expected to contain:
        - 'task_type'
        - 'raw_input'
        - 'context' (list of documents)
        - 'model_family'
        """
        model_family = enriched.get("model_family")
        context_snippets = enriched.get("context", [])
        context_block = "\n\n".join(str(c) for c in context_snippets) if context_snippets else ""

        system_prompt = (
            "You are an aligned assistant following a context engineering lifecycle. "
            "You must use provided context faithfully, indicate uncertainty, and keep within "
            "the requested tone and length."
        )
        user_prompt = enriched.get("raw_input", "")

        if context_block:
            user_prompt = f"Question:\n{user_prompt}\n\nRelevant context:\n{context_block}"

        formatted_prompt = self.formatter.format_prompt(
            model_family=model_family,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            metadata=enriched,
        )

        return {**enriched, "prompt": formatted_prompt}


@dataclass
class OutputServing:
    """
    OutputServing implements the Serving (output validation and refinement)
    stage of the lifecycle.

    It receives the model's raw output and applies:
    - quality checks (hallucination detection, format validation)
    - optional post-processing (e.g. trimming, citation normalisation)
    - structured response packaging for the caller
    """

    validator: Any

    def process(self, generated_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and package the model output.

        The `validator` is expected to expose a `validate(text: str, context: dict)`
        method returning a ValidationResult-like object.
        """
        validation_result = self.validator.validate(text=generated_text, context=context)
        response = {
            "output": generated_text,
            "validation": validation_result,
            "is_acceptable": validation_result.overall_score >= context.get(
                "quality_threshold", 0.8
            ),
        }
        return response
