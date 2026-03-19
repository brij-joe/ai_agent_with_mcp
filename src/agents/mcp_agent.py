import asyncio
import logging
import os
from datetime import timedelta

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.sse import sse_client

from app_constants import GEMINI_MODEL

# Load environment variables
load_dotenv(dotenv_path="c:\\temp\\.env", override=True)

# Configure environment
os.environ["vertexai"] = "False"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class MCPAgent:
    """Agent that integrates LangChain with MCP tools."""

    def __init__(self):
        self.mcp_client = None
        self.tools = None
        self._sse_cm = None
        self.agent = None
        self.session = None
        self.read_stream = None
        self.write_stream = None

    async def init_mcp_client(self):
        self.mcp_client = MultiServerMCPClient(
            {
                "default": {
                    "url": "http://localhost:8080/sse",
                    "transport": "sse",
                }
            }
        )


    async def get_tools(self):
        return await self.mcp_client.get_tools()

    async def init_agent(self) -> None:
        self.tools = await self.get_tools()
        llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL)
        self.agent = create_agent(llm, self.tools)
        logger.info("LangChain agent initialized with MCP tools.")


    def format_response(self, response):
        messages = response["messages"]
        # get last AI message
        for msg in reversed(messages):
            if msg.__class__.__name__ == "AIMessage":
                content = msg.content
                # Gemini returns list of content blocks
                if isinstance(content, list):
                    return "\n".join(
                        item.get("text", "") for item in content if item.get("type") == "text"
                    )
                return content
        return "No response found"

    async def ask(self, query: str) -> str:
        """Ask the agent a question and return its response."""
        prompt = f"""
        You are an AI agent with access to external tools via MCP.

        STRICT RULES:
        1. You MUST use tools when relevant.
        2. NEVER hallucinate.
        3. Prefer tools over internal knowledge.

        AVAILABLE TOOLS:
        {[tool.name for tool in self.tools]}

        User query:
        {query}
        """

        if not self.agent:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        model_response = await self.agent.ainvoke({"messages": [{"role": "user", "content": query}]})
        return self.format_response(response=model_response)

    async def close(self):
        self.mcp_client=None
        self.tools = None
        self.agent = None
        self.session = None
        self.read_stream = None
