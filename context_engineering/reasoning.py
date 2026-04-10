from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class ReasoningStrategy(str, Enum):
    """
    Seven reasoning strategies from the guidebook.

    - DIRECT_INSTRUCTION
    - CHAIN_OF_THOUGHT
    - STEP_BACK
    - TREE_OF_THOUGHT
    - REACT
    - SELF_CONSISTENCY
    - HIERARCHICAL_ORCHESTRATION
    """

    DIRECT_INSTRUCTION = "direct_instruction"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    STEP_BACK = "step_back"
    TREE_OF_THOUGHT = "tree_of_thought"
    REACT = "react"
    SELF_CONSISTENCY = "self_consistency"
    HIERARCHICAL_ORCHESTRATION = "hierarchical_orchestration"


@dataclass
class ReasoningStrategyConfig:
    name: ReasoningStrategy
    prompt_prefix: str


class ReasoningStrategySelector:
    """
    Selects and instantiates reasoning strategies given task type and complexity.

    This enables experiments with prompt-level reasoning control without tying
    the application to a single fixed style.
    """

    def select_strategy(
        self,
        task_type: str,
        complexity_level: Literal["low", "medium", "high"],
    ) -> ReasoningStrategyConfig:
        """
        Choose an appropriate reasoning strategy and prompt prefix.
        """
        task_type = task_type or "general"

        if task_type == "technical_documentation" and complexity_level in ("medium", "high"):
            strategy = ReasoningStrategy.CHAIN_OF_THOUGHT
            prefix = (
                "Use a clear chain-of-thought. First list the relevant APIs and concepts, "
                "then derive the structure of the documentation, and only then write the final answer."
            )
        elif task_type == "customer_service" and complexity_level == "low":
            strategy = ReasoningStrategy.DIRECT_INSTRUCTION
            prefix = (
                "Answer directly and concisely. Resolve the issue in as few steps as possible, "
                "while remaining polite and empathetic."
            )
        elif task_type == "research_analysis":
            strategy = ReasoningStrategy.STEP_BACK
            prefix = (
                "First restate the research question in your own words, then identify key sub-questions, "
                "then synthesise an evidence-based answer with citations."
            )
        elif complexity_level == "high":
            strategy = ReasoningStrategy.TREE_OF_THOUGHT
            prefix = (
                "Explore multiple solution paths. For each, briefly assess pros and cons, "
                "then choose the best path and follow it to a conclusion."
            )
        else:
            strategy = ReasoningStrategy.DIRECT_INSTRUCTION
            prefix = "Follow the instructions carefully and answer in a straightforward manner."

        if task_type == "research_analysis" and complexity_level == "high":
            strategy = ReasoningStrategy.SELF_CONSISTENCY
            prefix = (
                "Silently consider at least three different plausible answers, then choose the answer "
                "that is most consistent across them. Present only the final, consistent answer with citations."
            )

        return ReasoningStrategyConfig(name=strategy, prompt_prefix=prefix)
