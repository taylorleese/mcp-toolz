"""Tests for OpenAI client."""

from unittest.mock import MagicMock, patch

import pytest

from context_manager.openai_client import ChatGPTClient


class TestChatGPTClient:
    """Test ChatGPT client."""

    @patch("context_manager.openai_client.OpenAI")
    def test_init(self, mock_openai: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test ChatGPT client initialization."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        client = ChatGPTClient()
        assert client is not None
        assert client.model == "gpt-5.1"
        mock_openai.assert_called_once()

    def test_init_no_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test initialization fails without API key."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OpenAI API key"):
            ChatGPTClient()

    @patch("context_manager.openai_client.OpenAI")
    def test_get_second_opinion(self, mock_openai: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test getting a second opinion."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a good approach"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = ChatGPTClient()
        response = client.get_second_opinion("some code to review")

        assert response == "This is a good approach"
        assert mock_client.chat.completions.create.called

    @patch("context_manager.openai_client.OpenAI")
    def test_get_second_opinion_with_question(self, mock_openai: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test getting a second opinion with a custom question."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Yes, this is correct"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = ChatGPTClient()
        response = client.get_second_opinion("some code", "Is this correct?")

        assert response == "Yes, this is correct"

    @patch("context_manager.openai_client.OpenAI")
    def test_format_prompt(self, mock_openai: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test formatting prompt."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        mock_openai.return_value = MagicMock()

        client = ChatGPTClient()
        formatted = client._format_prompt("some context text")

        assert "some context text" in formatted
        assert "second opinion" in formatted

    @patch("context_manager.openai_client.OpenAI")
    def test_format_prompt_with_question(self, mock_openai: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test formatting prompt with a question."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        mock_openai.return_value = MagicMock()

        client = ChatGPTClient()
        formatted = client._format_prompt("some context text", "Is this correct?")

        assert "some context text" in formatted
        assert "Is this correct?" in formatted
