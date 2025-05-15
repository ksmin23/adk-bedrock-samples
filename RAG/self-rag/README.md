# Self-RAG using ADK

[Self-RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/) implementation using Google ADK (Agent Development Kit).

## Data Ingestion to Vector Store

1. Download source documents
   ```
   python3 utils/download_source_data.py
   ```

2. Ingest documents into the Vector Store

   (1) Chroma
   ```
   python3 utils/chroma_vector_store_builder.py
   ```

   (2) FAISS
   ```
   python3 utils/faiss_vector_store_builder.py
   ```

## References

 * [(GitHub) adk-selfrag](https://github.com/jeyong-shin/adk-selfrag)
 * [LangChain - Chroma](https://python.langchain.com/docs/integrations/vectorstores/chroma/)
 * [LangChain - FAISS](https://python.langchain.com/docs/integrations/vectorstores/faiss/)
 * [LangChain Open Tutorial](https://github.com/LangChain-OpenTutorial/LangChain-OpenTutorial)
 * [LangGraph Tutorails > Self-RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/)
