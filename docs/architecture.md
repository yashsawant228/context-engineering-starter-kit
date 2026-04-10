# Architecture

This document describes the architecture of the Context Engineering Starter Kit, inspired by microservices principles but delivered as a lightweight Python package.

## High-Level Components

- **Lifecycle Layer** — Implements the four-stage lifecycle:
  - `InputAnalysis`
  - `ContextRetrieval`
  - `ContextTransformation`
  - `OutputServing`
- **UCEF Orchestrator** — The `UCEF` class coordinates lifecycle stages, reasoning strategy selection, and hallucination validation.
- **Reasoning Layer** — `ReasoningStrategySelector` selects among seven reasoning strategies.
- **Hallucination Layer** — `HallucinationDetector` provides multi-type checks and confidence scores.
- **Model Formatting Layer** — `ModelFormatter` adapts prompts to the conventions of Claude, GPT-4o, Gemini, DeepSeek, and open-source models.
- **Configuration and Templates** — YAML configs and Markdown templates parameterise behaviour without code changes.

## Data Flow

