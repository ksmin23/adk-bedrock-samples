#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse

from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import DuckDuckGoSearchResults

from google.genai import types
from . import prompt

import litellm
# litellm._turn_on_debug()


def _render_reference(
  callback_context: CallbackContext,
  llm_response: LlmResponse,
) -> LlmResponse:
  """Appends grounding references to the response."""
  del callback_context
  if (
    not llm_response.content or
    not llm_response.content.parts or
    not llm_response.grounding_metadata
  ):
    return llm_response
  references = []
  for chunk in llm_response.grounding_metadata.grounding_chunks or []:
    title, uri, text = '', '', ''
    if chunk.retrieved_context:
      title = chunk.retrieved_context.title
      uri = chunk.retrieved_context.uri
      text = chunk.retrieved_context.text
    elif chunk.web:
      title = chunk.web.title
      uri = chunk.web.uri
    parts = [s for s in (title, text) if s]
    if uri and parts:
      parts[0] = f'[{parts[0]}]({uri})'
    if parts:
      references.append('* ' + ': '.join(parts) + '\n')
  if references:
    reference_text = ''.join(['\n\nReference:\n\n'] + references)
    llm_response.content.parts.append(types.Part(text=reference_text))
  if all(part.text is not None for part in llm_response.content.parts):
    all_text = '\n'.join(part.text for part in llm_response.content.parts)
    llm_response.content.parts[0].text = all_text
    del llm_response.content.parts[1:]
  return llm_response


# Instantiate LangChain tool
ddg_search = DuckDuckGoSearchResults(
  num_results=5,
)

# Wrap with LangchainTool
adk_ddg_tool = LangchainTool(tool=ddg_search)

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

critic_agent = LlmAgent(
  model=bedrock_model,
  name="critic_agent",
  instruction=prompt.CRITIC_PROMPT,
  tools=[adk_ddg_tool],
  after_model_callback=_render_reference,
)
