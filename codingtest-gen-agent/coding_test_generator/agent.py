#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Based on: https://github.com/jeyong-shin/adk-codingtest-gen-agent/blob/main/codingtest-generator/agent.py (retrieved 2025-05-19)

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import DuckDuckGoSearchResults

import litellm
# litellm._turn_on_debug()

from .prompts import INSTRUCTION
from .shared_lib.constants import CLAUDE_3_5_SONNET
from .shared_lib.constants import MAX_NUM_SEARCH_RESULTS
from .shared_lib.constants import STATE_ROOT_AGENT
from .sub_agents import problem_generator_loop_agent
from .sub_agents import problem_solver_agent
from .sub_agents import test_case_generator_agent
from .sub_agents import topic_finder_agent


# Instantiate LangChain tool
ddg_search = DuckDuckGoSearchResults(
  name='duckduckgo_search',
  num_results=MAX_NUM_SEARCH_RESULTS,
)

# Wrap with LangchainTool
adk_ddg_search = LangchainTool(tool=ddg_search)

model_id = CLAUDE_3_5_SONNET
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

# Create the main agent that will be used by both the CLI and ADK web
root_agent = LlmAgent(
  model=bedrock_model,
  name="codingtest_generator_agent",
  description="An agent that generates coding tests for software engineers.",
  instruction=INSTRUCTION,
  tools=[adk_ddg_search],
  sub_agents=[
    topic_finder_agent,
    problem_generator_loop_agent,
    problem_solver_agent,
    test_case_generator_agent
  ],
  output_key=STATE_ROOT_AGENT
)
