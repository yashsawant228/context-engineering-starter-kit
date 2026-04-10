from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class ModelFamily(str, Enum):
    CLAUDE = "claude"
    GPT4O = "gpt4o"
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"
    OPEN_SOURCE = "open_source"


CLAUDE_SYSTEM_TAG = "system"
CLAUDE_USER_TAG = "user"

GPT4O_SYSTEM_HEADER = "# System"
GPT4O_USER_HEADER = "## User"

GEMINI_CONTEXT_HEADER = "Context:"
GEMINI_TASK_HEADER = "Task:"
GEMINI_FORMAT_HEADER = "Format:"

DEEPSEEK_THINK_OPEN = "<think>"
DEEPSEEK_THINK_CLOSE = "</think>"

OPEN_SOURCE_ROLE_PREFIX = "[ROLE]"
OPEN_SOURCE_TASK_PREFIX = "[TASK]"
OPEN_SOURCE_OUTPUT_PREFIX = "[OUTPUT]"


@dataclass
class ModelFormatter:
    """
    ModelFormatter adapts prompts to each model family's preferred format:

    - Claude: XML-like tags.
    - GPT-4o: Markdown headings and clear sections.
    - Gemini: Context/Task/Format sections.
    - DeepSeek: CoT tags wrapping reasoning.
    - Open source: [ROLE][TASK][OUTPUT] framing.
    """

    def format_prompt(
        self,
        model_family: ModelFamily,
        system_prompt: str,
        user_prompt: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        metadata = metadata or {}
        if model_family == ModelFamily.CLAUDE:
            return self._format_claude(system_prompt, user_prompt)
        if model_family == ModelFamily.GPT4O:
            return self._format_gpt4o(system_prompt, user_prompt)
        if model_family == ModelFamily.GEMINI:
            return self._format_gemini(system_prompt, user_prompt, metadata)
        if model_family == ModelFamily.DEEPSEEK:
            return self._format_deepseek(system_prompt, user_prompt)
        return self._format_open_source(system_prompt, user_prompt, metadata)

    def _format_claude(self, system_prompt: str, user_prompt: str) -> str:
        return (
            f"<{CLAUDE_SYSTEM_TAG}>\n{system_prompt}\n</{CLAUDE_SYSTEM_TAG}>\n\n"
            f"<{CLAUDE_USER_TAG}>\n{user_prompt}\n</{CLAUDE_USER_TAG}>"
        )

    def _format_gpt4o(self, system_prompt: str, user_prompt: str) -> str:
        return (
            f"{GPT4O_SYSTEM_HEADER}\n{system_prompt}\n\n"
            f"{GPT4O_USER_HEADER}\n{user_prompt}\n"
        )

    def _format_gemini(
        self, system_prompt: str, user_prompt: str, metadata: Dict[str, Any]
    ) -> str:
        task_type = metadata.get("task_type", "general")
        output_format = metadata.get("output_format", "Plain text answer.")
        return (
            f"{GEMINI_CONTEXT_HEADER}\n{system_prompt}\n\n"
            f"{GEMINI_TASK_HEADER}\nTask type: {task_type}\nUser request:\n{user_prompt}\n\n"
            f"{GEMINI_FORMAT_HEADER}\n{output_format}\n"
        )

    def _format_deepseek(self, system_prompt: str, user_prompt: str) -> str:
        return (
            f"{DEEPSEEK_THINK_OPEN}\n"
            f"{system_prompt}\n\n"
            f"User request:\n{user_prompt}\n"
            f"{DEEPSEEK_THINK_CLOSE}"
        )

    def _format_open_source(
        self, system_prompt: str, user_prompt: str, metadata: Dict[str, Any]
    ) -> str:
        role = metadata.get("role", "Senior assistant")
        task = metadata.get("task_type", "general")
        return (
            f"{OPEN_SOURCE_ROLE_PREFIX} {role}\n"
            f"{OPEN_SOURCE_TASK_PREFIX} {task}\n"
            f"{OPEN_SOURCE_OUTPUT_PREFIX}\n"
            f"{system_prompt}\n\nUser request:\n{user_prompt}\n"
        )
