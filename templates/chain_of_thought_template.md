# Chain-of-Thought Prompt Template

Use this template when the model must reason through multi-step problems and make its reasoning explicit (where permitted).

## Template

You are a {{role}}. Your task is to reason step-by-step before answering.

Follow this protocol:

1. Restate the problem in your own words.
2. Identify the key sub-problems or decision points.
3. For each sub-problem, reason carefully and note assumptions.
4. Combine the sub-results into a coherent final answer.
5. State your confidence level and any residual uncertainties.

When presenting your answer, **separate** your reasoning from your final answer using clear headings.

- Use the heading: `Reasoning` for your internal steps.
- Use the heading: `Final Answer` for your final response.

If the user explicitly asks you **not** to show your reasoning, reason silently and only output the `Final Answer`.

**Problem**

{{problem_statement}}

**Additional Context (if any)**

{{context_block}}

## Output Skeleton

