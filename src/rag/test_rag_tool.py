from src.rag.rag_tool import search_company_documents


question = "What is the name of the candidate in the resume?"

result = search_company_documents(question)

print("\n========== RAG RESULT ==========\n")
print(result)