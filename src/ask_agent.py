import asyncio
import logging

from agents.mcp_agent import MCPAgent

# Configure logging
logging.basicConfig(level=logging.CRITICAL, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


async def interactive_loop() -> None:
    """Run an interactive loop to continuously accept user input."""
    agent = MCPAgent()
    await agent._init_mcp_client()
    await agent.init_agent()

    print("\n\nAI Agent is ready. Type 'exit' to quit.")
    while True:
        query = input("\n\n\nYou: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Exiting MCP Agent. Goodbye!")
            break
        if not query:
            continue
        try:
            response = await agent.ask(query)
            # Safely extract the last message if available
            messages = response.get("messages", [])
            if messages:
                last_message = messages[-1]
                logger.info("Last agent message: %s", last_message)
                print(f"Agent: {last_message}")
            else:
                logger.warning("No messages returned in response.")
                print("Agent: [No response]")
        except Exception as e:
            logger.exception("Error processing query: %s", e)


async def main() -> None:
    """Run an interactive loop to continuously accept user input."""
    agent = MCPAgent()
    await agent.init_mcp_client()
    await agent.init_agent()
    response = await agent.ask("What are some news headlines today in India?")
    print(f"Received response: \n\n{response}")
    await  agent.close()


if __name__ == "__main__":
    try:
        # asyncio.run(interactive_loop())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted. Shutting down.")

