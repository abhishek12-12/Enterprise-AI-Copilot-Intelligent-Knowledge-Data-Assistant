from src.rag.rag_tool import search_company_documents


def test_rag_query():
    question = "What is the name of the candidate in the resume?"

    result = search_company_documents.invoke(question)

    assert result
    assert "Abhishek" in result