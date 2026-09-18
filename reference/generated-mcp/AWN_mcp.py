"""Integrated verified AWN tools, running over MCP stdio."""
from fastmcp import FastMCP
from tools.cli_wrapper import cli_wrapper_mcp

mcp = FastMCP(name="AWN")
mcp.mount(cli_wrapper_mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")
