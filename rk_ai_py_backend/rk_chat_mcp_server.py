from fastmcp import FastMCP
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")  # Specify the path to your .env file
ricky_description = os.getenv("who_is_ricky")
mcp = FastMCP("RK chat MCP Server")

@mcp.tool()
def who_is_ricky() -> str:
    """Return information about Ricky."""
    return ricky_description


if __name__ == "__main__":
    mcp.run(transport="streamable-http",
            host="0.0.0.0", port=8001)
