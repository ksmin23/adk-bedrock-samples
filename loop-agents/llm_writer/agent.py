#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Source: https://github.com/google/adk-samples/blob/main/agents/llm-auditor/llm_auditor/agent.py

from google.adk.agents import (
  LoopAgent,
  SequentialAgent
)

from .shared_lib.constants import MAX_ITERATIONS
from .sub_agents.writer import initial_writer_agent
from .sub_agents.critic import critic_agent
from .sub_agents.refiner import refiner_agent


# Refinement Loop Agent
refinement_loop = LoopAgent(
  name="refinement_loop",
  # Agent order is crucial: Critique first, then Refine/Exit
  sub_agents=[
    critic_agent,
    refiner_agent
  ],
  max_iterations=MAX_ITERATIONS
)

# Overall Sequential Pipeline
# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = SequentialAgent(
  name="iterative_writing_pipeline",
  sub_agents=[
    initial_writer_agent,
    refinement_loop
  ],
  description=(
    "Writes an initial document and "
    "then iteratively refines it with critique using an exit tool."
  )
)
