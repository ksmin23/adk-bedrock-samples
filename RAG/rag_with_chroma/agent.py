#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma

import litellm
# litellm._turn_on_debug()

from typing import Any
from typing_extensions import override
from google.adk.tools.retrieval.base_retrieval_tool import BaseRetrievalTool
from google.adk.tools import ToolContext


class ChromaRetrieval(BaseRetrievalTool):
  """A retrieval tool that uses Chroma Retriever to retrieve data."""

  def __init__(
    self,
    *,
    name: str,
    description: str,
    persistent_path: str,
    collection_name: str,
    embedding_model_id: str='amazon.titan-embed-text-v2:0',
    region_name: str='us-east-1'
  ):
    super().__init__(name=name, description=description)

    self.persistent_path = persistent_path
    self.collection_name = collection_name

    embeddings = BedrockEmbeddings(
      model_id=embedding_model_id,
      region_name=region_name
    )

    print(f'Loading data from {self.persistent_path}')

    persist_db = Chroma(
      persist_directory=self.persistent_path,
      embedding_function=embeddings,
      collection_name=collection_name,
    )

    self.retriever = persist_db.as_retriever()


  @override
  async def run_async(
      self, *, args: dict[str, Any], tool_context: ToolContext
  ) -> Any:
    response = self.retriever.invoke(args['query'])
    return [doc.page_content for doc in response]


ask_chroma_retrieval = ChromaRetrieval(
  name='retrieve_rag_documentation',
  description=(
    'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
  ),
  persistent_path='./vector_store/chroma_db',
  collection_name='kb_for_rag'
)

model_id = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

instruction_prompt = """
You are an AI assistant with access to a specialized document corpus.
Use the ask_chroma_retrieval tool to answer specific knowledge-based questions by retrieving relevant information.
Do not use retrieval for casual or general conversation.

If the user's intent is unclear, ask clarifying questions before answering.
Only answer questions related to the corpus. If you cannot answer, explain why.

When responding, cite your sources at the end under "Citations" or "References."
- Use the retrieved chunk’s `title` (and section, if available).
- For web resources, include the full URL.
- Cite each file only once, even if multiple chunks are used.

Do not reveal your internal reasoning or retrieval process.
Provide concise, factual answers with appropriate citations.
If information is insufficient, state that clearly.
"""

root_agent = Agent(
  name="ask_rag_agent",
  model=bedrock_model,
  description=(
    "Agent to answer questions using retrieve_rag_documentation."
  ),
  instruction=instruction_prompt,
  tools=[ask_chroma_retrieval] # Add the wrapped tool here
)