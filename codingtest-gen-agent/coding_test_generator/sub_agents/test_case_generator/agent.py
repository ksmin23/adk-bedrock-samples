#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Based on: https://github.com/jeyong-shin/adk-codingtest-gen-agent/blob/main/codingtest-generator/sub_agents/test_case_generator/agent.py (retrieved 2025-05-19)

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

import litellm
# litellm._turn_on_debug()

from .prompts import INSTRUCTION
from ...shared_lib.constants import STATE_TEST_CASE_GENERATOR
from ...shared_lib.constants import LLAMA3_70B_INSTRUCT

model_id = LLAMA3_70B_INSTRUCT
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

test_case_generator_agent = LlmAgent(
  model=bedrock_model,
  name="test_case_generator_agent",
  description="An agent that generates python code that generates coding test test cases.",
  instruction=INSTRUCTION,
  output_key=STATE_TEST_CASE_GENERATOR
)