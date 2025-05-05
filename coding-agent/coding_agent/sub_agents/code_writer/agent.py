#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

import litellm
# litellm._turn_on_debug()

from ...shared_lib.prompts import CODE_WRITER_PROMPT

model_id = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

code_writer_agent = Agent(
  name="code_writer_agent",
  model=bedrock_model,
  description=(
    "Writes initial code based on a specification."
  ),
  instruction=CODE_WRITER_PROMPT,
  # Stores its output (the initial code) into the session state
  # under the key 'review_comments'.
  output_key="generated_code"
)
