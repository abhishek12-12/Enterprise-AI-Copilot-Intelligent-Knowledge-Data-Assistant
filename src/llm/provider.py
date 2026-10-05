import os

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI


def get_llm(provider: str = "ollama"):
    """
    Return the configured LLM provider.
    Ollama is the default so the project works without OpenAI credits.
    """

    if provider.lower() == "openai":
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not configured.")

        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    ollama_base_url = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
    )

    return ChatOllama(
    model="llama3.2",
    temperature=0,
    base_url=ollama_base_url
    )