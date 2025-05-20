#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Based on: https://github.com/jeyong-shin/adk-codingtest-gen-agent/blob/main/codingtest-generator/sub_agents/topic_finder/agent.py (retrieved 2025-05-19)

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

import litellm
# litellm._turn_on_debug()

from .prompts import INSTRUCTION
from ...shared_lib.constants import STATE_TOPIC_FINDER_AGENT
from ...shared_lib.constants import CLAUDE_3_HAIKU


model_id = CLAUDE_3_HAIKU
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

topic_finder_agent = LlmAgent(
  model=bedrock_model,
  name="topic_finder_agent",
  description="An agent that generates coding test topics.",
  instruction=INSTRUCTION,
  output_key=STATE_TOPIC_FINDER_AGENT
)