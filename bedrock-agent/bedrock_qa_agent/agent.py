#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

import litellm
# litellm._turn_on_debug()

model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
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

basic_agent = LlmAgent(
  model=bedrock_model,
  name="bedrock_qa_agent",
  instruction="You are a fast and helpful assistant.",
  tools=[],
)

root_agent = basic_agent

