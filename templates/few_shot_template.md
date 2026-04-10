# Few-Shot Prompt Template

This template structures task instructions with 2–5 diverse examples. Use it when a task benefits from pattern demonstration rather than abstract description.

## Template

**Instruction**

You are a {{role}}. Perform the task described below, following the examples.

Task: {{task_description}}

Constraints:
- Target audience: {{audience}}
- Length constraint: {{length_constraint}} (e.g. "under 300 words").
- Style: {{style}} (e.g. "formal", "conversational", "step-by-step").

**Examples**

Example 1 (canonical):
- Input: {{example_1_input}}
- Output: {{example_1_output}}

Example 2 (edge case):
- Input: {{example_2_input}}
- Output: {{example_2_output}}

Example 3 (optional, different modality or domain):
- Input: {{example_3_input}}
- Output: {{example_3_output}}

Example 4–5 (optional):
- Use sparingly; additional examples increase token usage and may reduce capacity for new context.

**User Input**

Now process the following input using the same pattern:

- Input: {{user_input}}

## Diversity Guidance

- Ensure examples cover the most important variants of the task (e.g. short vs long inputs, typical vs edge cases).
- Avoid examples that duplicate the same pattern with only superficial changes.
- Include at least one example that demonstrates how to handle ambiguous or incomplete input.

## Token Budget Advice

- Aim to keep the combined examples within 40–60% of the total context window when using retrieval; remaining tokens should be reserved for live context and the model's answer.
- Consider summarising long example outputs into high-signal patterns instead of full text where possible.
