from src.database.sql_tool import query_company_database


def test_sql_query():
    question = "How many employees are in Bangalore?"

    result = query_company_database.invoke(question)

    assert "3 employees" in result
    assert "Bangalore" in result