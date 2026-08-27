"""OpenAI-backed implementation support for Aegis Dev Agent."""

import json
import os

from openai import OpenAI


class AIClient:
    """Generate structured implementation changes."""

    def __init__(self, model: str = "gpt-5") -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        self.model = model
        self.client = OpenAI(api_key=api_key)

    def generate_patch(
        self,
        task: str,
        context: str,
    ) -> list[dict[str, str]]:
        """Ask the model for structured repository changes."""
        if not task.strip():
            raise ValueError("task must not be empty.")

        prompt = f"""
You are a coding agent working on the Air Aegis project.

Task:
{task}

Repository context:
{context}

Return ONLY valid JSON with this exact structure:

{{
  "changes": [
    {{
      "path": "relative/path.py",
      "content": "complete file content"
    }}
  ]
}}

Rules:
- Paths must be relative to the Air Aegis repository.
- Never use absolute paths.
- Never use '..' path components.
- Only modify files necessary for the requested task.
- Preserve existing project architecture.
- Do not include shell commands.
- Do not include markdown.
"""

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        raw = response.output_text.strip()

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Model returned invalid JSON."
            ) from exc

        changes = payload.get("changes")

        if not isinstance(changes, list):
            raise ValueError(
                "Model response does not contain a valid changes list."
            )

        return changes
