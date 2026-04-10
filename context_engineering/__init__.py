"""
Context Engineering Starter Kit

This package implements a lightweight version of the Universal Context Engineering
Framework (UCEF) described in "The Ultimate Context Engineering Guidebook", with
four lifecycle stages and supporting utilities for hallucination detection,
reasoning strategy selection, and model-specific prompt formatting.
"""

from .lifecycle import InputAnalysis, ContextRetrieval, ContextTransformation, OutputServing
from .ucef import UCEF
from .hallucination import HallucinationDetector, ValidationResult
from .reasoning import ReasoningStrategySelector, ReasoningStrategy
from .model_formatter import ModelFormatter, ModelFamily

__all__ = [
    "InputAnalysis",
    "ContextRetrieval",
    "ContextTransformation",
    "OutputServing",
    "UCEF",
    "HallucinationDetector",
    "ValidationResult",
    "ReasoningStrategySelector",
    "ReasoningStrategy",
    "ModelFormatter",
    "ModelFamily",
]

__version__ = "0.1.0"
