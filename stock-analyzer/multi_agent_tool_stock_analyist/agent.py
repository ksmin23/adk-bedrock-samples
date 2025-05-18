#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Based on: https://github.com/Engineer1999/Blog-Resources/blob/main/Multi-Agent-Stock-Analyist/agent.py (retrieved 2025-05-17)

import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import agent_tool

import litellm
# litellm._turn_on_debug()

from .shared_lib.prompts import SYNTHESIZER_INSTRUCTION
from .sub_agents.news import news_agent
from .sub_agents.history import historical_agent
from .sub_agents.economics import economic_agent
from .sub_agents.politics import political_agent


load_dotenv()

model_id = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

# Define the main synthesizer/orchestrator agent
root_agent = LlmAgent(
    model=bedrock_model,
    name="stock_analysis_synthesizer",
    description="Orchestrates specialized agents (as tools) to produce a comprehensive stock analysis and investment recommendation.",
    # Use AgentTool to make specialized agents available as tools
    tools=[
      agent_tool.AgentTool(agent=news_agent),
      agent_tool.AgentTool(agent=historical_agent),
      agent_tool.AgentTool(agent=economic_agent),
      agent_tool.AgentTool(agent=political_agent)
    ],
    instruction=SYNTHESIZER_INSTRUCTION,
    # Note: The root agent itself doesn't need tools if all data gathering is delegated.
    # The specialized agents have the necessary tools (e.g., duckduckgo_search).
)