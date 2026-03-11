"""Google Gemini API client for getting Gemini responses."""

import os

import google.generativeai as genai


class GeminiClient:
    """Client for interacting with Google's Gemini API."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        """Initialize the Gemini client."""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            msg = "Google API key must be provided or set in GOOGLE_API_KEY environment variable"
            raise ValueError(msg)

        self.model_name: str = model or os.getenv("MCP_TOOLZ_GEMINI_MODEL") or "gemini-2.5-flash"
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        self.timeout = 30.0

    def get_second_opinion(self, context: str, question: str | None = None) -> str:
        """Get Gemini's second opinion on a context, or answer a specific question.

        Args:
            context: The context text to analyze
            question: Optional specific question to ask. If None, provides general second opinion.
        """
        if question:
            system_instruction = """You are a senior software engineering consultant answering questions about code, \
architecture decisions, and implementation plans.

Provide clear, actionable answers based on the context provided."""
        else:
            system_instruction = """You are a senior software engineering consultant providing second opinions on code, \
architecture decisions, and implementation plans.

Your role is to:
- Provide constructive, balanced feedback
- Highlight both strengths and potential issues
- Suggest alternatives when appropriate
- Point out edge cases or security concerns
- Be concise but thorough

Format your response clearly with sections as needed."""

        user_content = self._format_prompt(context, question)

        model_with_instruction = genai.GenerativeModel(self.model_name, system_instruction=system_instruction)

        response = model_with_instruction.generate_content(user_content, request_options={"timeout": self.timeout})

        return str(response.text)

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
