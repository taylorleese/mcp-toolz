"""MCP server for multi-LLM tools."""

from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from context_manager.deepseek_client import DeepSeekClient
from context_manager.gemini_client import GeminiClient
from context_manager.openai_client import ChatGPTClient


class ContextMCPServer:
    """MCP server for multi-LLM tools."""

    def __init__(self) -> None:
        """Initialize the MCP server."""
        self.server = Server("mcp-toolz")

        # Register handlers
        self.server.list_tools()(self.list_tools)  # type: ignore[no-untyped-call]
        self.server.call_tool()(self.call_tool)

    async def list_tools(self) -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="ask_chatgpt",
                description="Ask ChatGPT a question about a context, or get a general second opinion",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "context": {"type": "string", "description": "The context text to analyze or ask about"},
                        "question": {
                            "type": "string",
                            "description": (
                                "Optional specific question to ask about the context. If not provided, gets a general second opinion."
                            ),
                        },
                    },
                    "required": ["context"],
                },
            ),
            Tool(
                name="ask_gemini",
                description="Ask Google Gemini a question about a context, or get a general second opinion",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "context": {"type": "string", "description": "The context text to analyze or ask about"},
                        "question": {
                            "type": "string",
                            "description": (
                                "Optional specific question to ask about the context. If not provided, gets a general second opinion."
                            ),
                        },
                    },
                    "required": ["context"],
                },
            ),
            Tool(
                name="ask_deepseek",
                description="Ask DeepSeek a question about a context, or get a general second opinion",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "context": {"type": "string", "description": "The context text to analyze or ask about"},
                        "question": {
                            "type": "string",
                            "description": (
                                "Optional specific question to ask about the context. If not provided, gets a general second opinion."
                            ),
                        },
                    },
                    "required": ["context"],
                },
            ),
        ]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Execute a tool call."""
        if name == "ask_chatgpt":
            context = arguments["context"]
            question = arguments.get("question")

            try:
                chatgpt_client = ChatGPTClient()
                response = chatgpt_client.get_second_opinion(context, question)

                header = "ChatGPT's Answer:" if question else "ChatGPT's Opinion:"
                return [TextContent(type="text", text=f"{header}\n\n{response}")]
            except ValueError as e:
                return [TextContent(type="text", text=f"Error: {e}")]

        if name == "ask_gemini":
            context = arguments["context"]
            question = arguments.get("question")

            try:
                gemini_client = GeminiClient()
                response = gemini_client.get_second_opinion(context, question)

                header = "Gemini's Answer:" if question else "Gemini's Opinion:"
                return [TextContent(type="text", text=f"{header}\n\n{response}")]
            except ValueError as e:
                return [TextContent(type="text", text=f"Error: {e}")]

        if name == "ask_deepseek":
            context = arguments["context"]
            question = arguments.get("question")

            try:
                deepseek_client = DeepSeekClient()
                response = deepseek_client.get_second_opinion(context, question)

                header = "DeepSeek's Answer:" if question else "DeepSeek's Opinion:"
                return [TextContent(type="text", text=f"{header}\n\n{response}")]
            except ValueError as e:
                return [TextContent(type="text", text=f"Error: {e}")]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    async def run(self) -> None:
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, self.server.create_initialization_options())
