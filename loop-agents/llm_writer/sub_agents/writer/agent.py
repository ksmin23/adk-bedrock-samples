#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

import litellm
litellm._turn_on_debug()

from ...shared_lib.constants import STATE_CURRENT_DOC
from ...shared_lib.prompts import WRITER_PROMPT

load_dotenv()

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

# Initial Writer Agent (Runs ONCE at the beginning)
initial_writer_agent = LlmAgent(
  name="initial_writer_agent",
  model=bedrock_model,
  # include_contents='none',
  instruction=WRITER_PROMPT,
  description=(
    "Writes the initial document draft based on the topic, "
    "aiming for some initial substance."
  ),
  output_key=STATE_CURRENT_DOC
)