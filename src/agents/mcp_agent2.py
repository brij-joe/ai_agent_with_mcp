import asyncio
import logging
import os
from typing import Optional

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
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

    def __init__(self) -> None:
        self.client = None
        self.agent = None

    async def init_mcp_client(self):
        self.client = MultiServerMCPClient(
            {
                "web_search": {
                    "url": "http://localhost:8080/sse",
                    "transport": "sse",
                },
            }
        )

    async def run_mcp_websearch(self, query: str):
        """Run a search query using the MCP backend."""
        if not self.mcp_session:
            raise RuntimeError("MCP session not initialized.")
        return await asyncio.wait_for(self.mcp_session.call_tool(name="web_search", arguments={"query": query}),
            timeout=10)

    async def read_mcp_resource(self, resource_name: str):
        if not self.mcp_session:
            raise RuntimeError("MCP session not initialized.")
        return await asyncio.wait_for(self.mcp_session.read_resource("resource://news_websites"), timeout=10)

    async def init_agent(self) -> None:
        """Initialize the LangChain agent with MCP tools."""
        mcp_websearch_tool = StructuredTool.from_function(coroutine=self.run_mcp_websearch, name="web_search",
            description="Search web for latest information")

        mcp_top_news_websites_tool = StructuredTool.from_function(coroutine=self.read_mcp_resource,
            name="top_news_websites", description="Get the top indian news website URL", )

        tools = [mcp_websearch_tool, mcp_top_news_websites_tool]
        llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL)
        llm_with_tools = llm.bind_tools(tools=tools, tool_choice="required")
        self.agent = create_agent(llm_with_tools, tools)
        logger.info("LangChain agent initialized with MCP tools.")

    async def ask(self, query: str) -> str:
        """Ask the agent a question and return its response."""
        if not self.agent:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        response = await self.agent.ainvoke({"messages": [{"role": "user", "content": query}]})
        return response
