#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

import litellm
# litellm._turn_on_debug()


def say_hello(name: str = "there") -> str:
  """Provides a simple greeting, optionally addressing the user by name.

  Args:
    name (str, optional): The name of the person to greet. Defaults to "there".

  Returns:
    str: A friendly greeting message.
  """

  print(f"--- Tool: say_hello called with name: {name} ---")
  return f"Hello, {name}!"


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

greeting_agent = Agent(
  name="greeting_agent",
  model=bedrock_model,
  description=(
    "Handles simple greetings and hellos using the 'say_hello' tool." # Crucial for delegation
  ),
  instruction=(
    "You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
    "Use the 'say_hello' tool to generate the greeting. "
    "If the user provides their name, make sure to pass it to the tool. "
    "Do not engage in any other conversation or tasks."
  ),
  tools=[say_hello]
)

root_agent = greeting_agent