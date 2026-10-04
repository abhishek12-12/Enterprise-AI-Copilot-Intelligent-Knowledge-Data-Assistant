from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


CHROMA_PATH = "chroma_db"


# 1. Load the same embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 2. Connect to existing ChromaDB
vector_store = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
    collection_name="enterprise_documents"
)


# 3. User question
question = "what is the name of the student?"


# 4. Perform similarity search
results = vector_store.similarity_search(
    question,
    k=3
)


# 5. Display retrieved chunks
print(f"\nQuestion: {question}")
print(f"Number of retrieved chunks: {len(results)}")


for i, document in enumerate(results):
    print(f"\n--- Retrieved Chunk {i + 1} ---")
    print(document.page_content)
    print("Metadata:", document.metadata)