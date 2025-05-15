#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Based on: https://github.com/jeyong-shin/adk-selfrag/blob/main/self-rag/agent.py (retrieved 2025-05-15)

import os

from dotenv import load_dotenv
from google.adk.agents import Agent, LlmAgent
from google.adk.models.lite_llm import LiteLlm

import litellm
# litellm._turn_on_debug()

from .shared_lib.retriever import ChromaRetrieval
from .shared_lib.custom_agent import SelfRagAgent

from .prompts import (
  GENERATE_INSTRUCTION,
  GRADE_DOCUMENT_INSTRUCTION,
  QUERY_REWRITER_INSTRUCTION,
  RETRIEVER_INSTRUCTION,
  HALLUCINATION_CHECK_INSTRUCTION,
  RELEVANCE_CHECK_INSTRUCTION,
)

load_dotenv()


ask_chroma_retrieval = ChromaRetrieval(
  name='retrieve_rag_documentation',
  description=(
    'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
  ),
  persistent_path='../vector_store/chroma_db',
  collection_name='kb_for_rag'
)

model_id = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

retriever = LlmAgent(
  name="Retriever",
  model=bedrock_model,
  description=(
    "This agent retrieves data from the vector database "
    "using retrieve_rag_documentation."
  ),
  instruction=RETRIEVER_INSTRUCTION,
  tools=[ask_chroma_retrieval],
  output_key="retriever_result"
)

grade_document = LlmAgent(
  name="GradeDocument",
  model=bedrock_model,
  description=(
    "This agent grades documents based on their relevance to a given query and user input."
  ),
  instruction=GRADE_DOCUMENT_INSTRUCTION,
  output_key="grade_document_result"
)

query_rewriter = LlmAgent(
  name="QueryRewriter",
  model=bedrock_model,
  description=(
    "This agent rewrites queries to improve their relevance."
  ),
  instruction=QUERY_REWRITER_INSTRUCTION,
  output_key="query"
)

generate = LlmAgent(
  name="Generate",
  model=bedrock_model,
  description=(
    "This agent generates answers based on the retrieved documents and user input."
  ),
  instruction=GENERATE_INSTRUCTION,
  output_key="generate_result"
)

hallucination_checker = LlmAgent(
  name="HallucinationChecker",
  model=bedrock_model,
  description=(
    "This agent checks for hallucinations in generated answers."
  ),
  instruction=HALLUCINATION_CHECK_INSTRUCTION,
  output_key="hallucination_check_result"
)

relevance_check = LlmAgent(
  name="RelevanceCheck",
  model=bedrock_model,
  description=(
    "This agent checks the relevance of generated answers."
  ),
  instruction=RELEVANCE_CHECK_INSTRUCTION,
  output_key="relevance_check_result"
)

root_agent = SelfRagAgent(
  name="SelfRAGAgent",
  description=(
    "This agent performs self-retrieval-augmented generation."
  ),
  retriever=retriever,
  document_grader=grade_document,
  query_rewriter=query_rewriter,
  generator=generate,
  hallucination_checker=hallucination_checker,
  relevance_checker=relevance_check,
  output_key="self_rag_result"
)
