
# Documentation Retrieval Agent

This agent is designed to answer questions related to documents you uploaded to Vector store such as [Chroma](https://python.langchain.com/docs/integrations/vectorstores/chroma/), [FAISS](https://python.langchain.com/docs/integrations/vectorstores/faiss/).

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

 * [LangChain - Chroma](https://python.langchain.com/docs/integrations/vectorstores/chroma/)
 * [LangChain - FAISS](https://python.langchain.com/docs/integrations/vectorstores/faiss/)
 * [LangChain Open Tutorial](https://github.com/LangChain-OpenTutorial/LangChain-OpenTutorial)
