import logging
import os
import random

import psycopg2
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# This is a simple MCP server implementation that demonstrates how to create a singleton server instance,
# register tools, resources, and prompts, and interact with a PostgreSQL database. The server can be extended
# with additional functionality as needed.
class MServer:
    _instance = None
    def __new__(cls, server_name: str, host: str, port: int):
        if cls._instance is None:
            cls._instance = super(MServer, cls).__new__(cls)
        return cls._instance

    def __init__(self, server_name: str = "MyMCPServer", host: str = "localhost", port: int = 8080):
        if not hasattr(self, '_initialized'):
            self.server_name = server_name
            self.host = host
            self.port = port
            self._init_server()
            self._init_tavily()
            self._init_database()
            self._init_defaults()
            self._initialized = True
            self.is_running = False
            logger.info(f"MCP server is initialized with server_name: {self.server_name}, host: {self.host}, and port: {self.port}.")

    def _init_server(self):
        # Initialize server
        self.mcp = FastMCP(name=self.server_name, host=self.host, port=self.port)
        logger.info("Created FastMCP object ...")

    def _init_tavily(self):
        # Initialize Tavily client
        self.tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
        logger.info(f"Created tavily client ...")

    def _init_database(self):
        # Initialize database connection
        self.conn = psycopg2.connect(
            host=os.environ.get("dbhost"),
            database=os.environ.get("dbname"),
            user=os.environ.get("dbuser"),
            password=os.environ.get("dbpass")
        )
        self.cursor = self.conn.cursor()
        logger.info(f"Database connection created ...")

    def _init_defaults(self):
        @self.mcp.tool(
            name="web_search",
            title="Web Search Tool",
            description="Search the web for a given query using Tavily API.",
            meta={"version": "1.0", "author": "Brij Joe"}
        )
        def web_search(query: str):
            print(f">>>>>>>>>> Searching web for query: {query}")
            results = self.tavily_client.search(query, topic="general", max_results=3)
            print(f">>>>>>>>>> Web Search Found {len(results)} results.")
            return str(results)

        @self.mcp.tool(
            name="top_3_news_website",
            title="Top 10 News Websites",
            description="Get top 3 list of popular news websites.",
            meta={"version": "1.0", "author": "Brij Joe"}
        )
        def random_news_website( k: int = 3):
            print(f">>>>>>>> Getting top 3 Indian news websites")
            indian_news_websites = [
                "https://timesofindia.indiatimes.com",
                "https://www.ndtv.com",
                "https://www.thehindu.com",
                "https://indianexpress.com",
                "https://www.hindustantimes.com",
                "https://www.indiatoday.in",
                "https://zeenews.india.com",
                "https://www.news18.com",
                "https://www.deccanherald.com",
                "https://economictimes.indiatimes.com"
            ]
            selected_sites = random.sample(indian_news_websites, 3)
            print(f">>>>>>> Found random 3 websites: {selected_sites}")
            return selected_sites

        @self.mcp.prompt(
            name="greeting",
            title="Greeting Prompt",
            description="Generate a greeting message for a given name."
        )
        def greeting(name: str):
            return f"Hello {name}, welcome to GenAI world!"

    # Registering tools manually at runtime
    def add_tool(self, name: str, func):
        """
        Dynamically add a tool.
        Example:
            server.add_tool("add_numbers", lambda a, b: a + b)
        """
        self.mcp.tool(name=name)(func)

    # Registering resources manually at runtime
    def add_resource(self, uri: str, func):
        """
        Dynamically add a resource.
        Example:
            server.add_resource("resource://random_words", lambda: ["apple", "banana"])
        """
        self.mcp.resource(uri)(func)

    # Registering prompts manually at runtime
    def add_prompt(self, name: str, func):
        """
        Dynamically add a prompt.
        Example:
            server.add_prompt("greeting", lambda name: f"Hello {name}")
        """
        self.mcp.prompt(name)(func)

    def add_database_resource(self, uri: str, query: str):
        """
        Dynamically add a resource backed by a database query.
        Example:
            server.add_database_resource("resource://db_words", "SELECT word FROM words")
        """

        def db_resource():
            self.cursor.execute(query)
            return [row[0] for row in self.cursor.fetchall()]

        self.mcp.resource(uri)(db_resource)

    def run(self):
        if self.is_running:
            logger.info("MCP server is already running.")
            return
        logger.info("Starting MCP Server ...")
        self.mcp.run(transport="sse")
