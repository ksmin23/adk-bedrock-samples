#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Based on: https://github.com/Engineer1999/Blog-Resources/blob/main/Basic-Stock-Analyzer/agent.py (retrieved 2025-05-17)

import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import DuckDuckGoSearchResults

import litellm
# litellm._turn_on_debug()

from ...shared_lib.prompts import HISTORICAL_AGENT_INSTRUCTION


load_dotenv()

# Instantiate LangChain tool
ddg_search = DuckDuckGoSearchResults(
  num_results=5,
)

# Wrap with LangchainTool
adk_ddg_search = LangchainTool(tool=ddg_search)

model_id = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-haiku-20240307-v1:0')
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

# Create the main agent that will be used by both the CLI and ADK web
historical_agent = LlmAgent(
  model=bedrock_model,
  name="historical_stock_analyst",
  description="Analyzes the historical stock performance of a company.",
  instruction=HISTORICAL_AGENT_INSTRUCTION,
  tools=[adk_ddg_search]
)