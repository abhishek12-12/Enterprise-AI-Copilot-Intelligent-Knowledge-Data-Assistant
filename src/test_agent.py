from src.agents.agent import ask_agent


def test_sql_question():
    result = ask_agent("How many employees are in Bangalore?")
    assert "3 employees" in result


def test_mongo_question():
    result = ask_agent("Tell me about Rahul's skills.")
    assert "Python" in result


def test_rag_question():
    result = ask_agent("What skills are mentioned in my resume?")
    assert len(result) > 0