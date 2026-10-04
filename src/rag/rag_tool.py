from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool


CHROMA_PATH = "chroma_db"


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
    collection_name="enterprise_documents"
)


retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

@tool
def search_company_documents(question: str) -> str:
    """
    Search the company knowledge base and return
    the most relevant document content.
    """

    documents = retriever.invoke(question)

    if not documents:
        return "No relevant information was found."

    results = []

    for document in documents:
        source = document.metadata.get("source", "Unknown")
        page = document.metadata.get("page", "Unknown")

        results.append(
            f"Source: {source}, Page: {page}\n"
            f"Content: {document.page_content}"
        )

    return "\n\n".join(results)