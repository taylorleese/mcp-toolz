"""OpenAI API client for getting ChatGPT responses."""

import os

from openai import OpenAI


class ChatGPTClient:
    """Client for interacting with OpenAI's ChatGPT API."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        """Initialize the ChatGPT client."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            msg = "OpenAI API key must be provided or set in OPENAI_API_KEY environment variable"
            raise ValueError(msg)

        self.model: str = model or os.getenv("MCP_TOOLZ_MODEL") or "gpt-5.1"
        self.client = OpenAI(api_key=self.api_key, timeout=30.0)

    def get_second_opinion(self, context: str, question: str | None = None) -> str:
        """Get ChatGPT's second opinion on a context, or answer a specific question.

        Args:
            context: The context text to analyze
            question: Optional specific question to ask. If None, provides general second opinion.
        """
        if question:
            system_prompt = """You are a senior software engineering consultant answering questions about code, \
architecture decisions, and implementation plans.

Provide clear, actionable answers based on the context provided."""
        else:
            system_prompt = """You are a senior software engineering consultant providing second opinions on code, \
architecture decisions, and implementation plans from Claude Code.

Your role is to:
- Provide constructive, balanced feedback
- Highlight both strengths and potential issues
- Suggest alternatives when appropriate
- Point out edge cases or security concerns
- Be concise but thorough

Format your response clearly with sections as needed."""

        user_content = self._format_prompt(context, question)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )

        return response.choices[0].message.content or ""

    def _format_prompt(self, context: str, question: str | None = None) -> str:
        """Format context and optional question into a prompt.

        Args:
            context: The context text
            question: Optional specific question to append
        """
        parts = [f"# Context\n\n{context}"]

        if question:
            parts.append(f"\n---\n**Question:** {question}")
        else:
            parts.append("\n---\nPlease provide a second opinion on the above context.")

        return "\n".join(parts)
