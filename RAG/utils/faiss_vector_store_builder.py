#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os
import boto3
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS


def main():
  source_data_dir = os.path.join(os.path.dirname(__file__), "../data")
  loader = TextLoader(f"{source_data_dir}/01-vectorstore-retriever-appendix-keywords.txt", encoding="utf-8")
  documents = loader.load()

  text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
  split_docs = text_splitter.split_documents(documents) # Split into smaller chunks

  region_name = boto3.Session().region_name
  embeddings = BedrockEmbeddings(
    model_id='amazon.titan-embed-text-v2:0',
    region_name=region_name
  )

  faiss_db = FAISS.from_documents(split_docs, embeddings)
  folder_path = os.path.join(os.path.dirname(__file__), "../vector_store/faiss_db")
  faiss_db.save_local(folder_path=folder_path, index_name="faiss_index")

  print(f"\n{len(split_docs)} documents are stored in {folder_path}")


if __name__ == '__main__':
  main()
