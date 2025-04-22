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


# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
  """Gets tools from the File System MCP Server."""
  print("Attempting to connect to MCP Filesystem server...")
  tools, exit_stack = await MCPToolset.from_server(
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
  print("MCP Toolset created successfully.")
  # MCP requires maintaining a connection to the local MCP Server.
  # exit_stack manages the cleanup of this connection.
  return tools, exit_stack


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
    name='filesystem_assistant',
    instruction='Help user interact with the local filesystem using available tools.',
    tools=tools, # Provide the MCP tools to the ADK agent
  )

  return agent, exit_stack

root_agent = create_agent()
