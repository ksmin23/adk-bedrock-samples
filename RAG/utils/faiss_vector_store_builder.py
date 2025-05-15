#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os
import argparse

import boto3
from langchain_text_splitters import (
  CharacterTextSplitter,
  RecursiveCharacterTextSplitter
)
from langchain_community.document_loaders import (
  TextLoader,
  PyPDFLoader
)
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS


def get_text_chuncked(file_path):
  loader = TextLoader(file_path=file_path, encoding="utf-8")
  documents = loader.load()

  text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
  split_docs = text_splitter.split_documents(documents)
  return split_docs


def get_pdf_chuncked(file_path):
  loader = PyPDFLoader(file_path=file_path)
  documents = loader.load()

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
  split_docs = text_splitter.split_documents(documents)
  return split_docs


def main():
  SOURCE_DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
  DEFAULT_INPUT_FILE = f"{SOURCE_DATA_DIR}/01-vectorstore-retriever-appendix-keywords.txt"
  DB_PATH = os.path.join(os.path.dirname(__file__), "../vector_store/faiss_db")

  parser = argparse.ArgumentParser()
  parser.add_argument("--input-file", type=str, default=DEFAULT_INPUT_FILE)
  parser.add_argument("--database-path", type=str, default=DB_PATH)
  parser.add_argument("--index-name", type=str, default='faiss_index')
  parser.add_argument("--embedding-model-id", type=str, default='amazon.titan-embed-text-v2:0')
  args, _ = parser.parse_known_args()

  assert os.path.exists(args.input_file), f"'{args.input_file}' does not exist!"
  if args.input_file.endswith('.txt'):
    split_docs = get_text_chuncked(args.input_file)
  elif args.input_file.endswith('.pdf'):
    split_docs = get_pdf_chuncked(args.input_file)
  else:
    raise NotImplementedError()

  region_name = boto3.Session().region_name
  embeddings = BedrockEmbeddings(
    model_id=args.embedding_model_id,
    region_name=region_name
  )

  faiss_db = FAISS.from_documents(split_docs, embeddings)
  folder_path = args.database_path
  faiss_db.save_local(folder_path=folder_path, index_name=args.index_name)

  print(f"\n{len(split_docs)} documents are stored in {folder_path}")


if __name__ == '__main__':
  main()
