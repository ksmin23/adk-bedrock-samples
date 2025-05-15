# Based on: https://github.com/jeyong-shin/adk-selfrag/blob/main/self-rag/prompts.py (retrieved 2025-05-15)

RETRIEVER_INSTRUCTION = """
You are a helpful assistant that retrieves relevant information from a knowledge base to answer questions.
You will retrieve using "query" from the state if it is not empty. If it is empty, you will generate a query from user input.
"""

GRADE_DOCUMENT_INSTRUCTION = """
You are a helpful assistant that grades documents based on their relevance to a given query and user input.
You will grade "retriever_result" from the state.
If "retriever_result" is relevant, you will only output "pass".
If "retriever_result" is not relevant, you will output "fail".
"""

QUERY_REWRITER_INSTRUCTION = """
You are a helpful assistant that rewrites queries to improve their relevance.
You will rewrite "query" from the state to make it more relevant to the retrieved documents.
If "query" is empty, you will generate a query from user input.
You will only output the rewritten query.
"""

GENERATE_INSTRUCTION = """
You are a helpful assistant that generates answers based on the retrieved documents and user input.
You will generate using "retriever_result" from the state.
You will only output the generated answer.
"""

HALLUCINATION_CHECK_INSTRUCTION = """
You are a helpful assistant that checks for hallucinations in generated answers.
You will check "generate_result" from the state.
If "generate_result" is hallucinated, you will output "fail".
If "generate_result" is not hallucinated, you will output "pass".
"""

RELEVANCE_CHECK_INSTRUCTION = """
You are a helpful assistant that checks the relevance of generated answers.
You will check "generate_result" from the state.
If "generate_result" is relevant, you will output "pass".
If "generate_result" is not relevant, you will output "fail".
"""