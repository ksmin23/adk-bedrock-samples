#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Source: https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/fastmcp/simple_echo.py

"""
FastMCP Echo Server
"""

from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("Echo Server")


@mcp.tool()
def echo(text: str) -> str:
  """Echo the input text"""
  return text


# if __name__ == "__main__":
#   print("Launching MCP Server...")
#   try:
#     mcp.run(transport='stdio')
#   except KeyboardInterrupt:
#     print("\nMCP Server stopped by user.")
#   except Exception as e:
#     print(f"MCP Server encountered an error: {e}")
#   finally:
#     print("MCP Server process exiting.")