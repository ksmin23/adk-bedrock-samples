#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

import litellm
# litellm._turn_on_debug()


def say_goodbye() -> str:
  """Provides a simple farewell message to conclude the conversation."""

  print(f"--- Tool: say_goodbye called ---")
  return "Goodbye! Have a great day."


model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model,
#   model_config={
#     'temperature': 0.7,
#     'top_p': 0.9,
#     'top_k': 250,
#     'max_tokens': 2000
#   }
)

farewell_agent = Agent(
  name="farewell_agent",
  model=bedrock_model,
  description=(
    "Handles simple farewells and goodbyes using the 'say_goodbye' tool." # Crucial for delegation
  ),
  instruction=(
    "You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
    "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
    "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
    "Do not perform any other actions."
  ),
  tools=[say_goodbye]
)