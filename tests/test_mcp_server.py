"""Tests for MCP server functionality."""

from unittest.mock import MagicMock, patch

import pytest

from mcp_server.server import ContextMCPServer


@pytest.mark.integration
class TestMCPServerTools:
    """Test MCP server tool handlers."""

    @pytest.fixture
    def mcp_server(self) -> ContextMCPServer:
        """Create an MCP server instance."""
        return ContextMCPServer()

    @pytest.mark.asyncio
    async def test_list_tools(self, mcp_server: ContextMCPServer) -> None:
        """Test listing available tools."""
        tools = await mcp_server.list_tools()

        assert len(tools) == 4
        tool_names = [t.name for t in tools]
        assert "ask_chatgpt" in tool_names
        assert "ask_claude" in tool_names
        assert "ask_gemini" in tool_names
        assert "ask_deepseek" in tool_names

    @pytest.mark.asyncio
    @patch("mcp_server.server.ChatGPTClient")
    async def test_ask_chatgpt_tool(
        self,
        mock_chatgpt_class: MagicMock,
        mcp_server: ContextMCPServer,
    ) -> None:
        """Test the ask_chatgpt tool with mocked API."""
        mock_client = MagicMock()
        mock_client.get_second_opinion = MagicMock(return_value="Mocked ChatGPT response")
        mock_chatgpt_class.return_value = mock_client

        result = await mcp_server.call_tool("ask_chatgpt", {"context": "some code to review"})

        assert result is not None
        assert "Mocked ChatGPT response" in result[0].text
        mock_client.get_second_opinion.assert_called_once_with("some code to review", None)

    @pytest.mark.asyncio
    @patch("mcp_server.server.ChatGPTClient")
    async def test_ask_chatgpt_with_question(
        self,
        mock_chatgpt_class: MagicMock,
        mcp_server: ContextMCPServer,
    ) -> None:
        """Test the ask_chatgpt tool with a specific question."""
        mock_client = MagicMock()
        mock_client.get_second_opinion = MagicMock(return_value="Answer to question")
        mock_chatgpt_class.return_value = mock_client

        result = await mcp_server.call_tool("ask_chatgpt", {"context": "some code", "question": "Is this correct?"})

        assert result is not None
        assert "ChatGPT's Answer:" in result[0].text
        assert "Answer to question" in result[0].text
        mock_client.get_second_opinion.assert_called_once_with("some code", "Is this correct?")

    @pytest.mark.asyncio
    @patch("mcp_server.server.ClaudeClient")
    async def test_ask_claude_tool(
        self,
        mock_claude_class: MagicMock,
        mcp_server: ContextMCPServer,
    ) -> None:
        """Test the ask_claude tool with mocked API."""
        mock_client = MagicMock()
        mock_client.get_second_opinion = MagicMock(return_value="Mocked Claude response")
        mock_claude_class.return_value = mock_client

        result = await mcp_server.call_tool("ask_claude", {"context": "some code to review"})

        assert result is not None
        assert "Mocked Claude response" in result[0].text

    @pytest.mark.asyncio
    @patch("mcp_server.server.GeminiClient")
    async def test_ask_gemini_tool(
        self,
        mock_gemini_class: MagicMock,
        mcp_server: ContextMCPServer,
    ) -> None:
        """Test the ask_gemini tool with mocked API."""
        mock_client = MagicMock()
        mock_client.get_second_opinion = MagicMock(return_value="Mocked Gemini response")
        mock_gemini_class.return_value = mock_client

        result = await mcp_server.call_tool("ask_gemini", {"context": "some code to review"})

        assert result is not None
        assert "Mocked Gemini response" in result[0].text

    @pytest.mark.asyncio
    @patch("mcp_server.server.DeepSeekClient")
    async def test_ask_deepseek_tool(
        self,
        mock_deepseek_class: MagicMock,
        mcp_server: ContextMCPServer,
    ) -> None:
        """Test the ask_deepseek tool with mocked API."""
        mock_client = MagicMock()
        mock_client.get_second_opinion = MagicMock(return_value="Mocked DeepSeek response")
        mock_deepseek_class.return_value = mock_client

        result = await mcp_server.call_tool("ask_deepseek", {"context": "some code to review"})

        assert result is not None
        assert "Mocked DeepSeek response" in result[0].text

    @pytest.mark.asyncio
    @patch("mcp_server.server.ChatGPTClient")
    async def test_ask_chatgpt_error_handling(
        self,
        mock_chatgpt_class: MagicMock,
        mcp_server: ContextMCPServer,
    ) -> None:
        """Test ask_chatgpt error handling."""
        mock_client = MagicMock()
        mock_client.get_second_opinion = MagicMock(side_effect=ValueError("API key missing"))
        mock_chatgpt_class.return_value = mock_client

        result = await mcp_server.call_tool("ask_chatgpt", {"context": "some code"})

        assert result is not None
        assert "error" in result[0].text.lower()

    @pytest.mark.asyncio
    @patch("mcp_server.server.ClaudeClient")
    async def test_ask_claude_error_handling(
        self,
        mock_claude_class: MagicMock,
        mcp_server: ContextMCPServer,
    ) -> None:
        """Test ask_claude error handling."""
        mock_client = MagicMock()
        mock_client.get_second_opinion = MagicMock(side_effect=ValueError("API key missing"))
        mock_claude_class.return_value = mock_client

        result = await mcp_server.call_tool("ask_claude", {"context": "some code"})

        assert result is not None
        assert "error" in result[0].text.lower()

    @pytest.mark.asyncio
    @patch("mcp_server.server.GeminiClient")
    async def test_ask_gemini_error_handling(
        self,
        mock_gemini_class: MagicMock,
        mcp_server: ContextMCPServer,
    ) -> None:
        """Test ask_gemini error handling."""
        mock_client = MagicMock()
        mock_client.get_second_opinion = MagicMock(side_effect=ValueError("API key missing"))
        mock_gemini_class.return_value = mock_client

        result = await mcp_server.call_tool("ask_gemini", {"context": "some code"})

        assert result is not None
        assert "error" in result[0].text.lower()

    @pytest.mark.asyncio
    @patch("mcp_server.server.DeepSeekClient")
    async def test_ask_deepseek_error_handling(
        self,
        mock_deepseek_class: MagicMock,
        mcp_server: ContextMCPServer,
    ) -> None:
        """Test ask_deepseek error handling."""
        mock_client = MagicMock()
        mock_client.get_second_opinion = MagicMock(side_effect=ValueError("API key missing"))
        mock_deepseek_class.return_value = mock_client

        result = await mcp_server.call_tool("ask_deepseek", {"context": "some code"})

        assert result is not None
        assert "error" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_unknown_tool(self, mcp_server: ContextMCPServer) -> None:
        """Test calling an unknown tool."""
        result = await mcp_server.call_tool("unknown_tool_name", {})

        assert result is not None
        assert "unknown" in result[0].text.lower()
