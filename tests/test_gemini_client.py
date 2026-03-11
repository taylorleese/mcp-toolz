"""Tests for Google Gemini client."""

from unittest.mock import MagicMock, patch

import pytest

from context_manager.gemini_client import GeminiClient


class TestGeminiClient:
    """Test Gemini client."""

    @patch("context_manager.gemini_client.genai.configure")
    @patch("context_manager.gemini_client.genai.GenerativeModel")
    def test_init(self, mock_model: MagicMock, mock_configure: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test Gemini client initialization."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
        client = GeminiClient()
        assert client is not None
        assert client.model_name == "gemini-2.5-flash"
        mock_configure.assert_called_once_with(api_key="test-key")
        mock_model.assert_called_once()

    def test_init_no_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test initialization fails without API key."""
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        with pytest.raises(ValueError, match="Google API key"):
            GeminiClient()

    @patch("context_manager.gemini_client.genai.configure")
    @patch("context_manager.gemini_client.genai.GenerativeModel")
    def test_get_second_opinion(self, mock_model: MagicMock, mock_configure: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test getting a second opinion."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key")

        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "This is a solid implementation"
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance

        client = GeminiClient()
        response = client.get_second_opinion("some code to review")

        assert response == "This is a solid implementation"
        assert mock_instance.generate_content.called

    @patch("context_manager.gemini_client.genai.configure")
    @patch("context_manager.gemini_client.genai.GenerativeModel")
    def test_get_second_opinion_with_question(
        self, mock_model: MagicMock, mock_configure: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test getting a second opinion with a custom question."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key")

        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Yes, this approach is correct"
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance

        client = GeminiClient()
        response = client.get_second_opinion("some code", "Is this correct?")

        assert response == "Yes, this approach is correct"

    @patch("context_manager.gemini_client.genai.configure")
    @patch("context_manager.gemini_client.genai.GenerativeModel")
    def test_format_prompt(self, mock_model: MagicMock, mock_configure: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test formatting prompt."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key")

        client = GeminiClient()
        formatted = client._format_prompt("some context text")

        assert "some context text" in formatted
        assert "second opinion" in formatted

    @patch("context_manager.gemini_client.genai.configure")
    @patch("context_manager.gemini_client.genai.GenerativeModel")
    def test_format_prompt_with_question(self, mock_model: MagicMock, mock_configure: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test formatting prompt with a question."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key")

        client = GeminiClient()
        formatted = client._format_prompt("some context text", "Is this correct?")

        assert "some context text" in formatted
        assert "Is this correct?" in formatted
