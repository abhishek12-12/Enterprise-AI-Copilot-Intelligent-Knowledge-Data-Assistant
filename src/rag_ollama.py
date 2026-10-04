from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate


# -----------------------------
# 1. Load embeddings
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------
# 2. Load ChromaDB
# -----------------------------
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings,
    collection_name="enterprise_documents"
)


# -----------------------------
# 3. Create retriever
# -----------------------------
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# -----------------------------
# 4. Load local Ollama LLM
# -----------------------------
llm = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=0
)


# -----------------------------
# 5. RAG prompt
# -----------------------------
prompt = ChatPromptTemplate.from_template(
    """
You are an AI assistant answering questions about a candidate's resume.

Use ONLY the information provided in the context.

If the answer is not present in the context, say:
"I could not find that information in the document."

Context:
{context}

Question:
{question}

Answer:
"""
)


# -----------------------------
# 6. Ask question
# -----------------------------
question = input("\nAsk a question about the document: ")


# Retrieve relevant chunks
documents = retriever.invoke(question)

context = "\n\n".join(
    document.page_content for document in documents
)


# Create prompt
formatted_prompt = prompt.format(
    context=context,
    question=question
)


# Generate answer locally
response = llm.invoke(formatted_prompt)


print("\nAnswer:")
print(response.content)