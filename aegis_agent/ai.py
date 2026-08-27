"""OpenAI-backed implementation support for Aegis Dev Agent."""

import os

from openai import OpenAI


class AIClient:
    """Generate implementation plans and patches using an OpenAI model."""

    def __init__(self, model: str = "gpt-5") -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        self.model = model
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """Generate model output for a development request."""
        if not prompt.strip():
            raise ValueError("prompt must not be empty.")

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text
