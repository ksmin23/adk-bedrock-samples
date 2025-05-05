#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Source: https://github.com/google/adk-samples/blob/main/agents/llm-auditor/llm_auditor/agent.py

from google.adk.agents import SequentialAgent

from .sub_agents.critic import critic_agent
from .sub_agents.reviser import reviser_agent


llm_auditor = SequentialAgent(
  name="llm_auditor",
  description=(
    'Evaluates LLM-generated answers, verifies actual accuracy using the web,'
    ' and refines the response to ensure alignment with real-world'
    ' knowledge.'
  ),
  sub_agents=[critic_agent, reviser_agent]
)

root_agent = llm_auditor
