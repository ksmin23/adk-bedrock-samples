#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import DuckDuckGoSearchResults

import litellm
litellm._turn_on_debug()


# Instantiate LangChain tool
ddg_search = DuckDuckGoSearchResults(
  num_results=5,
)

# Wrap with LangchainTool
adk_ddg_tool = LangchainTool(tool=ddg_search)

model_id = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

root_agent = Agent(
  name="langchain_tool_agent",
  model=bedrock_model,
  description=(
    "Agent to answer questions using DuckDuckGoSearch."
  ),
  instruction=(
    "I can answer your questions by searching the internet."
    " Just ask me anything!"
  ),
  tools=[adk_ddg_tool] # Add the wrapped tool here
)