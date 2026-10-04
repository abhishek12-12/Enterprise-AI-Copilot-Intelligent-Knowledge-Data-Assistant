from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


PDF_PATH = "Data\Abhishek H B Resume.pdf"
CHROMA_PATH = "chroma_db"


# 1. Load PDF
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

print(f"Number of pages: {len(documents)}")


# 2. Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Number of chunks: {len(chunks)}")


# 3. Create embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 4. Create ChromaDB vector store
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_PATH,
    collection_name="enterprise_documents"
)


print("ChromaDB created successfully!")
print(f"Vector store location: {CHROMA_PATH}")