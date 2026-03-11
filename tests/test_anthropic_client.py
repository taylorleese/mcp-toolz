"""Tests for Anthropic client."""

from unittest.mock import MagicMock, patch

import pytest
from anthropic.types import TextBlock

from context_manager.anthropic_client import ClaudeClient


class TestClaudeClient:
    """Test Claude client."""

    @patch("context_manager.anthropic_client.Anthropic")
    def test_init(self, mock_anthropic: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test Claude client initialization."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        client = ClaudeClient()
        assert client is not None
        assert client.model == "claude-sonnet-4-5-20250929"
        mock_anthropic.assert_called_once()

    def test_init_no_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test initialization fails without API key."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(ValueError, match="Anthropic API key"):
            ClaudeClient()

    @patch("context_manager.anthropic_client.Anthropic")
    def test_get_second_opinion(self, mock_anthropic: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test getting a second opinion."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_text_block = MagicMock(spec=TextBlock)
        mock_text_block.text = "This looks good to me"
        mock_response.content = [mock_text_block]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        client = ClaudeClient()
        response = client.get_second_opinion("some code to review")

        assert response == "This looks good to me"
        assert mock_client.messages.create.called

    @patch("context_manager.anthropic_client.Anthropic")
    def test_get_second_opinion_with_question(self, mock_anthropic: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test getting a second opinion with a custom question."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_text_block = MagicMock(spec=TextBlock)
        mock_text_block.text = "Yes, that's correct"
        mock_response.content = [mock_text_block]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        client = ClaudeClient()
        response = client.get_second_opinion("some code", "Is this right?")

        assert response == "Yes, that's correct"

    @patch("context_manager.anthropic_client.Anthropic")
    def test_format_prompt(self, mock_anthropic: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test formatting prompt."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        mock_anthropic.return_value = MagicMock()

        client = ClaudeClient()
        formatted = client._format_prompt("some context text")

        assert "some context text" in formatted
        assert "second opinion" in formatted

    @patch("context_manager.anthropic_client.Anthropic")
    def test_format_prompt_with_question(self, mock_anthropic: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test formatting prompt with a question."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        mock_anthropic.return_value = MagicMock()

        client = ClaudeClient()
        formatted = client._format_prompt("some context text", "Is this correct?")

        assert "some context text" in formatted
        assert "Is this correct?" in formatted
