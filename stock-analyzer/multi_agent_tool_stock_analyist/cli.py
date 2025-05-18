#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Based on: https://github.com/Engineer1999/Blog-Resources/blob/main/Basic-Stock-Analyzer/cli.py (retrieved 2025-05-17)

import argparse
import asyncio
import time

from dotenv import load_dotenv
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from .agent import root_agent

load_dotenv()


async def analyze_stock(company_name: str):
  """Analyze a stock using the Multi-Agent Stock Analyst."""

  # Set up session
  session_service = InMemorySessionService()
  session = session_service.create_session(
    app_name="multi_agent_stock_analyzer",
    user_id="cli_user"
  )

  # Set up runner
  runner = Runner(
    app_name="multi_agent_stock_analyzer",
    agent=root_agent,
    session_service=session_service
  )

  # Create query
  query = f"Analyze {company_name} stock. Should I invest in it? Provide a comprehensive analysis."
  content = types.Content(
    role='user',
    parts=[types.Part(text=query)]
  )

  print(f"\n📊 Analyzing {company_name} ...")
  print("This may take a few minutes as we gather and analyze data.")

  # Process events and collect final response
  result = ""
  search_count = 0

  async for event in runner.run_async(
    session_id=session.id,
    user_id='cli_user',
    new_message=content
  ):
    # Track search operations
    if hasattr(event, 'content') and hasattr(event.content, 'parts'):
      for part in event.content.parts:
        if hasattr(part, 'function_call') and hasattr(part.function_call, 'name'):
          if part.function_call.name:
            search_count += 1
            print(f"🔍 Search #{search_count}: Finding information using '{part.function_call.name}' ...")
        elif hasattr(part, 'function_response'):
          print(f"✅ Search result received")

    # Get final response
    if hasattr(event, 'is_final_response') and event.is_final_response:
      if hasattr(event, 'content') and hasattr(event.content, 'parts'):
        for part in event.content.parts:
          if hasattr(part, 'text') and part.text:
            result += part.text

  return result


async def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--company",
    type=str,
    required=True,
    help="a company name to analyze (e.g., Google)")

  args, _ = parser.parse_known_args()

  try:
    start_time = time.time()
    result = await analyze_stock(args.company)
    end_time = time.time()

    print("\n============================================")
    print(f"ANALYSIS COMPLETED IN {round(end_time - start_time, 1)} SECONDS")
    print("============================================")

    print(result)
  except Exception as ex:
    print(f"\n❌ Error during analysis: {str(ex)}")
    import traceback
    traceback.print_exc()


if __name__ == '__main__':
  asyncio.run(main())
