#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Based on: https://github.com/jeyong-shin/adk-codingtest-gen-agent/blob/main/codingtest-generator/sub_agents/problem_loop/agent.py (retrieved 2025-05-19)

from google.adk.agents import BaseAgent, LoopAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from typing import AsyncGenerator

from ..problem_generator import problem_generator_agent
from ..problem_critic import problem_critic_agent
from ..problem_quality_checker import problem_quality_checker_agent
from ...shared_lib.constants import MAX_ITERATIONS


class CheckStatusAndEscalate(BaseAgent):
  async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    status = ctx.session.state.get('problem_quality_checker_output', 'fail')
    should_stop = (status == 'pass')
    yield Event(author=self.name, actions=EventActions(escalate=should_stop))


problem_generator_loop_agent = LoopAgent(
  name="problem_loop_agent",
  description="A loop agent that generates coding problems.",
  max_iterations=MAX_ITERATIONS,
  sub_agents=[
    problem_generator_agent,
    problem_critic_agent,
    problem_quality_checker_agent,
    CheckStatusAndEscalate(name='stop_checker')
  ]
)
