"""Tests for DeepSeek client."""

from unittest.mock import MagicMock, patch

import pytest

from context_manager.deepseek_client import DeepSeekClient


class TestDeepSeekClient:
    """Test DeepSeek client."""

    @patch("context_manager.deepseek_client.OpenAI")
    def test_init(self, mock_openai: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test DeepSeek client initialization."""
        monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
        client = DeepSeekClient()
        assert client is not None
        assert client.model == "deepseek-chat"
        mock_openai.assert_called_once_with(api_key="test-key", base_url="https://api.deepseek.com", timeout=30.0)

    def test_init_no_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test initialization fails without API key."""
        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        with pytest.raises(ValueError, match="DeepSeek API key"):
            DeepSeekClient()

    @patch("context_manager.deepseek_client.OpenAI")
    def test_get_second_opinion(self, mock_openai: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test getting a second opinion."""
        monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This code looks efficient"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = DeepSeekClient()
        response = client.get_second_opinion("some code to review")

        assert response == "This code looks efficient"
        assert mock_client.chat.completions.create.called

    @patch("context_manager.deepseek_client.OpenAI")
    def test_get_second_opinion_with_question(self, mock_openai: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test getting a second opinion with a custom question."""
        monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Yes, the implementation is optimal"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = DeepSeekClient()
        response = client.get_second_opinion("some code", "Is this optimal?")

        assert response == "Yes, the implementation is optimal"

    @patch("context_manager.deepseek_client.OpenAI")
    def test_format_prompt(self, mock_openai: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test formatting prompt."""
        monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
        mock_openai.return_value = MagicMock()

        client = DeepSeekClient()
        formatted = client._format_prompt("some context text")

        assert "some context text" in formatted
        assert "second opinion" in formatted

    @patch("context_manager.deepseek_client.OpenAI")
    def test_format_prompt_with_question(self, mock_openai: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test formatting prompt with a question."""
        monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
        mock_openai.return_value = MagicMock()

        client = DeepSeekClient()
        formatted = client._format_prompt("some context text", "Is this correct?")

        assert "some context text" in formatted
        assert "Is this correct?" in formatted
