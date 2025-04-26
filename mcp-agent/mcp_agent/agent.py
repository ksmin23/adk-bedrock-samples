#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os

from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import (
  MCPToolset,
  # SseServerParams,
  StdioServerParameters
)

import litellm
# litellm._turn_on_debug()

load_dotenv()

# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
  """Gets tools from MCP Servers."""
  print("Attempting to connect to load_web_page MCP server...")
  load_web_page_tools, exit_stack = await MCPToolset.from_server(
    # Use StdioServerParameters for local process communication
    connection_params=StdioServerParameters(
      command='python3', # Command to run the server
      args=[
        f"{os.environ['MCP_SERVER_PATH']}/adk_mcp_server.py"
      ],
    )
    # For remote servers, you would use SseServerParams instead:
    # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
  )
  print("Load Web Page MCP Toolset created successfully.")

  print("Attempting to connect to Echo MCP server...")
  echo_tools, echo_exit_stack = await MCPToolset.from_server(
    # Use StdioServerParameters for local process communication
    connection_params=StdioServerParameters(
      command='fastmcp', # Command to run the server
      args=[
        "run",
        f"{os.environ['MCP_SERVER_PATH']}/simple_echo.py"
      ],
    )
    # For remote servers, you would use SseServerParams instead:
    # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
  )
  print("Echo MCP Toolset created successfully.")

  # MCP requires maintaining a connection to the local MCP Server.
  # exit_stack manages the cleanup of this connection.
  return load_web_page_tools + echo_tools, [exit_stack, echo_exit_stack]


async def create_agent():
  """Gets tools from MCP Server."""
  tools, exit_stack = await get_tools_async()

  model_id = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
  model = f'bedrock/{model_id}'
  bedrock_model = LiteLlm(
    model=model,
    model_config={
      'temperature': 0.7,
      'top_p': 0.9,
      'top_k': 250,
      'max_tokens': 2000
    }
  )

  agent = LlmAgent(
    model=bedrock_model,
    name='mcp_tools_assistant',
    instruction='Help user using available tools.',
    tools=tools, # Provide the MCP tools to the ADK agent
  )

  return agent, exit_stack

root_agent = create_agent()
