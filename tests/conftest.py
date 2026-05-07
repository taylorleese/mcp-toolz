"""Shared pytest fixtures for all tests."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from context_manager.openai_client import ChatGPTClient


@pytest.fixture
def mock_openai_client() -> ChatGPTClient:
    """Create a mock OpenAI client for testing."""
    client = MagicMock(spec=ChatGPTClient)
    client.query = AsyncMock(return_value="This is a mocked ChatGPT response")
    return client


@pytest.fixture
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up mock environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("MCP_TOOLZ_MODEL", "gpt-5")
