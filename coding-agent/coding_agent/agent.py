#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

from google.adk.agents import SequentialAgent
from google.adk.models.lite_llm import LiteLlm

import litellm
# litellm._turn_on_debug()

from .sub_agents.code_writer import code_writer_agent
from .sub_agents.code_reviewer import code_reviewer_agent
from .sub_agents.code_refactorer import code_refactorer_agent


code_pipeline_agent = SequentialAgent(
  name="coding_agent",
  sub_agents=[code_writer_agent, code_reviewer_agent, code_refactorer_agent]
)

root_agent = code_pipeline_agent
