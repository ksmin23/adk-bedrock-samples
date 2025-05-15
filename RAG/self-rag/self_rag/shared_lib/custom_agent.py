#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Based on: https://github.com/jeyong-shin/adk-selfrag/blob/main/self-rag/custom_agent.py (retrieved 2025-05-15)

from google.adk.agents import (
  BaseAgent,
  LlmAgent,
  SequentialAgent
)
from google.adk.events import (
  Event,
  EventActions
)

import time
from typing import AsyncGenerator
from typing_extensions import override

from logging import getLogger

logger = getLogger(__name__)


class SelfRagAgent(BaseAgent):
  retriever: LlmAgent
  document_grader: LlmAgent
  query_rewriter: LlmAgent
  generator: LlmAgent
  hallucination_checker: LlmAgent
  relevance_checker: LlmAgent

  retrieve_and_grade: SequentialAgent
  generate_and_hallucination_check: SequentialAgent

  output_key: str


  def __init__(
    self,
    name: str,
    description: str,
    retriever: LlmAgent,
    document_grader: LlmAgent,
    query_rewriter: LlmAgent,
    generator: LlmAgent,
    hallucination_checker: LlmAgent,
    relevance_checker: LlmAgent,
    output_key: str="self_rag_result"
  ):
    retrieve_and_grade = SequentialAgent(
      name="RetrieveAndGrade",
      sub_agents=[retriever, document_grader]
    )

    generate_and_hallucination_check = SequentialAgent(
      name="GenerateAndHallucinationCheck",
      sub_agents=[generator, hallucination_checker]
    )

    sub_agents = [
      retrieve_and_grade,
      generate_and_hallucination_check,
      query_rewriter,
      relevance_checker
    ]

    super().__init__(
      name=name,
      description=description,
      retriever=retriever,
      document_grader=document_grader,
      query_rewriter=query_rewriter,
      generator=generator,
      hallucination_checker=hallucination_checker,
      relevance_checker=relevance_checker,
      retrieve_and_grade=retrieve_and_grade,
      generate_and_hallucination_check=generate_and_hallucination_check,
      sub_agents=sub_agents,
      output_key=output_key
    )


  @override
  async def _run_async_impl(self, ctx) -> AsyncGenerator[Event, None]:
    logger.info(f"[{self.name}] Running Self-RAG agent")

    max_retry = 5
    for _ in range(max_retry):
      async for event in self.retrieve_and_grade.run_async(ctx):
        logger.info(f"[{self.name}] Event from retrive and grade: {event.model_dump_json(indent=2, exclude_none=True)}")
        yield event

      grade_document_result = ctx.session.state.get("grade_document_result")
      grade_document_result = grade_document_result.lower().strip()

      if grade_document_result == "fail":
        logger.info(f"[{self.name}] Document grading failed, retrying...")
        async for event in self.query_rewriter.run_async(ctx):
          logger.info(f"[{self.name}] Event from query rewriter: {event.model_dump_json(indent=2, exclude_none=True)}")
          yield event
        continue

      logger.info(f"[{self.name}] Document grading succeeded, proceeding to generation and hallucination check")
      for _ in range(max_retry):
        async for event in self.generate_and_hallucination_check.run_async(ctx):
          logger.info(f"[{self.name}] Event from generate and hallucination check: {event.model_dump_json(indent=2, exclude_none=True)}")
          yield event

        hallucination_check_result = ctx.session.state.get("hallucination_check_result")
        hallucination_check_result = hallucination_check_result.lower().strip()
        if hallucination_check_result == "pass":
          break

      async for event in self.relevance_checker.run_async(ctx):
        logger.info(f"[{self.name}] Event from relevence checker: {event.model_dump_json(indent=2, exclude_none=True)}")
        yield event

      relevance_check_result = ctx.session.state.get("relevance_check_result")
      relevance_check_result = relevance_check_result.lower().strip()

      if relevance_check_result == "fail":
        logger.info(f"[{self.name}] Relevance check failed, retrying...")
        async for event in self.query_rewriter.run_async(ctx):
          logger.info(f"[{self.name}] Event from query rewriter: {event.model_dump_json(indent=2, exclude_none=True)}")
          yield event
        continue
      else:
        logger.info(f"[{self.name}] Relevance check succeeded, stopping agent")
        break
    else:
      logger.info(f"[{self.name}] Max retry reached, stopping agent")

    yield Event(
      invocation_id="self_rag_finished",
      author="agent",
      actions=EventActions(
        state_delta={
          self.output_key: ctx.session.state.get("generate_result")
        }
      ),
      timestamp=time.time()
    )
