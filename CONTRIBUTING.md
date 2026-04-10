# Contributing to Context Engineering Starter Kit

Thank you for contributing to this context engineering toolkit. The goal is to keep the repository lean, high-signal, and production ready. Please read these guidelines before opening an issue or pull request.

## Ways to Contribute

- Bug reports and small fixes.
- New examples or improvements to existing examples.
- Enhancements to configs, templates, and docs that improve clarity, safety, or usability.
- Lightweight integrations (e.g. CI workflows) that support quality and reliability.

## Branching Strategy

- Default branch: `main` (always stable and releasable).
- Feature branches: `feat/<short-description>` (e.g. `feat/azure-openai-config`).
- Fix branches: `fix/<short-description>` (e.g. `fix/hallucination-score-bug`).
- Documentation branches: `docs/<short-description>`.

Avoid long-lived branches; keep changes focused and incremental.

## Commit Message Convention

Use concise, present-tense messages:

- `feat: add GPT-4o function-calling config`
- `fix: handle empty context in lifecycle`
- `docs: expand hallucination defence section`
- `chore: bump dependencies`

Limit each commit to a coherent set of changes.

## Pull Request Checklist

Before opening a PR:

- Ensure code is formatted with `black` and passes `ruff` lint checks (if installed).
- Run relevant examples to confirm nothing has regressed.
- Update or add documentation where behaviour changes.
- Add tests where logic becomes more complex (if you introduce non-trivial code).

Your PR description should include:

- A short summary of the change.
- Motivation and context (what problem it solves).
- Any breaking changes or migration notes.
- How you tested the change.

## Code Review Standards

Reviewers will look for:

- Alignment with the context engineering lifecycle and UCEF abstractions.
- Clear separation of concerns between lifecycle, UCEF, hallucination, reasoning, and formatting.
- Conservative defaults that prioritise correctness and safety over flashy behaviour.
- British English spelling in documentation and comments.
- Minimal, focused additions — no unnecessary abstractions or boilerplate.

Be prepared to iterate; review is a collaboration, not a gate.

## Issue Reporting

When raising an issue, please include:

- Environment details (Python version, OS, dependency versions).
- Steps to reproduce.
- Expected vs actual behaviour.
- Relevant snippets of configuration or code (sanitised — no secrets).

## Code of Conduct

By participating in this project, you agree to interact respectfully, assume good intent, and keep feedback specific and actionable.
