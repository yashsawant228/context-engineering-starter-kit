from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .hallucination import HallucinationDetector
from .lifecycle import ContextRetrieval, ContextTransformation, InputAnalysis, OutputServing
from .model_formatter import ModelFamily, ModelFormatter
from .reasoning import ReasoningStrategySelector


@dataclass
class UCEF:
    """
    Universal Context Engineering Framework (UCEF).

    Orchestrates the four core modules from the guidebook:
    - InputAnalysisModule
    - ContextEngineeringEngine (retrieval + transformation + reasoning)
    - QualityValidationSystem
    - IterativeRefinementProtocol

    This implementation focuses on being understandable and easily extended,
    rather than exhaustive.
    """

    input_analysis: InputAnalysis
    context_retrieval: ContextRetrieval
    context_transformation: ContextTransformation
    output_serving: OutputServing
    reasoning_selector: ReasoningStrategySelector
    hallucination_detector: HallucinationDetector

    @classmethod
    def default(cls) -> "UCEF":
        """
        Build a UCEF instance with default wiring using the provided components.

        This is suitable for quick-start experiments and examples. For production
        usage, construct UCEF explicitly and inject your own retrievers,
        formatters, and validators.
        """
        formatter = ModelFormatter()
        hallucination_detector = HallucinationDetector()
        input_analysis = InputAnalysis()
        retrieval = ContextRetrieval()
        transformation = ContextTransformation(formatter=formatter)
        output_serving = OutputServing(validator=hallucination_detector)
        reasoning_selector = ReasoningStrategySelector()
        return cls(
            input_analysis=input_analysis,
            context_retrieval=retrieval,
            context_transformation=transformation,
            output_serving=output_serving,
            reasoning_selector=reasoning_selector,
            hallucination_detector=hallucination_detector,
        )

    def run_pipeline(
        self,
        user_input: str,
        model_family: ModelFamily,
        metadata: Dict[str, Any],
        llm_callable: Any,
    ) -> Dict[str, Any]:
        """
        Execute the full UCEF pipeline:

        1. Analyse input.
        2. Select reasoning strategy.
        3. Retrieve context.
        4. Construct model-ready prompt (with reasoning prefix).
        5. Call the LLM.
        6. Validate and package output.

        :param user_input: Raw user request.
        :param model_family: Model family identifier.
        :param metadata: Additional control signals (e.g. domain, thresholds).
        :param llm_callable: A callable that accepts a prompt string and returns text.
        """
        # 1. Input analysis
        profile = self.input_analysis.process(user_input=user_input, metadata=metadata)
        profile["model_family"] = model_family

        # 2. Reasoning strategy
        strategy = self.reasoning_selector.select_strategy(
            task_type=profile["task_type"],
            complexity_level=metadata.get("complexity_level", "medium"),
        )
        profile["reasoning_strategy"] = strategy

        # 3. Context retrieval
        enriched = self.context_retrieval.process(profile)

        # 4. Prompt construction with reasoning prefix
        transformed = self.context_transformation.process(enriched)
        prompt = f"{strategy.prompt_prefix}\n\n{transformed['prompt']}"

        # 5. Call the LLM
        raw_output = llm_callable(prompt)

        # 6. Validation and packaging
        quality_threshold = metadata.get("quality_threshold", 0.8)
        transformed["quality_threshold"] = quality_threshold
        result = self.output_serving.process(generated_text=raw_output, context=transformed)

        # 7. Simple iterative refinement protocol (single retry on low score)
        if not result["is_acceptable"]:
            retry_prompt = (
                f"{prompt}\n\n"
                "The previous answer did not meet quality thresholds. "
                "Revise your answer, ensuring higher factual accuracy and clearer structure."
            )
            retry_output = llm_callable(retry_prompt)
            retry_result = self.output_serving.process(
                generated_text=retry_output, context=transformed
            )
            # Choose better of the two based on overall score
            if retry_result["validation"].overall_score >= result["validation"].overall_score:
                return {**retry_result, "attempts": 2}
            return {**result, "attempts": 2}

        return {**result, "attempts": 1}
