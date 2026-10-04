import os

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI


# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")


CHROMA_PATH = "chroma_db"


# 1. Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 2. Connect to existing ChromaDB
vector_store = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
    collection_name="enterprise_documents"
)


# 3. Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# 4. Create OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# 5. Ask the user a question
question = input("\nAsk a question about the document: ")


# 6. Retrieve relevant documents
documents = retriever.invoke(question)


# 7. Combine retrieved chunks into context
context = "\n\n".join(
    document.page_content
    for document in documents
)


# 8. Create prompt
prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using ONLY the
provided context.

If the answer cannot be found in the context,
say:

"I could not find the answer in the provided documents."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""


# 9. Send prompt to OpenAI
response = llm.invoke(prompt)


# 10. Display answer
print("\n================ ANSWER ================\n")
print(response.content)


# 11. Display sources
print("\n================ SOURCES ================\n")

for i, document in enumerate(documents):
    print(
        f"Source {i + 1}: "
        f"{document.metadata.get('source')} "
        f"(page {document.metadata.get('page')})"
    )