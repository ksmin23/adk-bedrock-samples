#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.models.lite_llm import LiteLlm

from . import prompt

import litellm
# litellm._turn_on_debug()

_END_OF_EDIT_MARK = '---END-OF-EDIT---'


def _remove_end_of_edit_mark(
  callback_context: CallbackContext,
  llm_response: LlmResponse,
) -> LlmResponse:
  del callback_context  # unused
  if not llm_response.content or not llm_response.content.parts:
    return llm_response
  for idx, part in enumerate(llm_response.content.parts):
    if _END_OF_EDIT_MARK in part.text:
      del llm_response.content.parts[idx + 1 :]
      part.text = part.text.split(_END_OF_EDIT_MARK, 1)[0]
  return llm_response


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

reviser_agent = LlmAgent(
  model=bedrock_model,
  name="reviser_agent",
  instruction=prompt.REVISER_PROMPT,
  after_model_callback=_remove_end_of_edit_mark,
)
