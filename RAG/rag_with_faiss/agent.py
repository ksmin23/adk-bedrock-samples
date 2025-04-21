#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings

import litellm
# litellm._turn_on_debug()

from typing import Any
from typing_extensions import override
from google.adk.tools.retrieval.base_retrieval_tool import BaseRetrievalTool
from google.adk.tools import ToolContext


class FAISSRetrieval(BaseRetrievalTool):
  """A retrieval tool that uses FAISS Retriever to retrieve data."""

  def __init__(self, *, name: str, description: str, input_dir: str, index_name: str):
    super().__init__(name=name, description=description)

    self.input_dir = input_dir
    self.index_name = index_name

    embeddings = BedrockEmbeddings(
      model_id='amazon.titan-embed-text-v2:0',
      region_name='us-east-1'
    )

    print(f'Loading data from {self.input_dir}')

    db = FAISS.load_local(
      folder_path=self.input_dir,
      embeddings=embeddings,
      index_name=self.index_name,
      allow_dangerous_deserialization=True
    )

    self.retriever = db.as_retriever()


  @override
  async def run_async(
      self, *, args: dict[str, Any], tool_context: ToolContext
  ) -> Any:
    response = self.retriever.invoke(args['query'])
    return [doc.page_content for doc in response]


ask_faiss_retrieval = FAISSRetrieval(
  name='retrieve_rag_documentation',
  description=(
    'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
  ),
  input_dir='./vector_store/faiss_db',
  index_name='faiss_index'
)

model_id = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
model = f'bedrock/{model_id}'
bedrock_model = LiteLlm(
  model=model
)

instruction_prompt = """
You are an AI assistant with access to a specialized document corpus.
Use the ask_faiss_retrieval tool to answer specific knowledge-based questions by retrieving relevant information.
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
  tools=[ask_faiss_retrieval] # Add the wrapped tool here
)