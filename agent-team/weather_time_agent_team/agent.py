#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

import litellm
# litellm._turn_on_debug()

from .sub_agents.farewell import farewell_agent
from .sub_agents.greeting import greeting_agent


def get_weather(city: str) -> dict:
  """Retrieves the current weather report for a specified city.

  Args:
      city (str): The name of the city for which to retrieve the weather report.

  Returns:
      dict: status and result or error msg.
  """
  if city.lower() == "new york":
    return {
      "status": "success",
      "report": (
        "The weather in New York is sunny with a temperature of 25 degrees"
        " Celsius (41 degrees Fahrenheit)."
      )
    }
  else:
    return {
      "status": "error",
      "error_message": f"Weather information for '{city}' is not available."
    }

def get_current_time(city: str) -> dict:
  """Returns the current time in a specified city.

  Args:
      city (str): The name of the city for which to retrieve the current time.

  Returns:
      dict: status and result or error msg.
  """

  if city.lower() == "new york":
    tz_identifier = "America/New_York"
  else:
    return {
      "status": "error",
      "error_message": (
        f"Sorry, I don't have timezone information for {city}."
      )
    }

  tz = ZoneInfo(tz_identifier)
  now = datetime.datetime.now(tz)
  report = (
    f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
  )
  return {"status": "success", "report": report}

model_id = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

root_agent = Agent(
  name="weather_time_agent_v2",
  model=bedrock_model,
  description=(
    "The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists."
  ),
  instruction=(
    "You are the main Weather and Time Agent coordinating a team. Your primary responsibility is to provide weather and time information. "
    "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in New York'). "
    "Use the 'get_current_time' tool ONLY for specific time requests (e.g., 'time in New York'). "
    "You have specialized sub-agents: "
    "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
    "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
    "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
    "If it's a weather request, handle it yourself using 'get_weather'. "
    "If it's a time request, handle it yourself using 'get_current_time'. "
    "For anything else, respond appropriately or state you cannot handle it."
  ),
  tools=[get_weather, get_current_time], # Root agent still needs the weather tool for its core task
  sub_agents=[greeting_agent, farewell_agent], # Link the sub-agents here!
)
