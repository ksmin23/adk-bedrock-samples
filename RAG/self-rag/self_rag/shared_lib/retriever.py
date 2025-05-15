#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

from logging import getLogger

# import os
# from google.adk.agents import Agent
# from google.adk.models.lite_llm import LiteLlm
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma

# import litellm
# litellm._turn_on_debug()

from typing import Any
from typing_extensions import override
from google.adk.tools.retrieval.base_retrieval_tool import BaseRetrievalTool
from google.adk.tools import ToolContext

logger = getLogger(__name__)


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

    # print(f'Loading data from {self.persistent_path}')
    logger.info(f'Loading data from {self.persistent_path}')

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
