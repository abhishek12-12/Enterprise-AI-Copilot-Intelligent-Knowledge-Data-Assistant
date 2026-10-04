from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


PDF_PATH = "Data\Abhishek H B Resume.pdf"


# 1. Load PDF
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()


# 2. Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Number of chunks: {len(chunks)}")


# 3. Load Hugging Face embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 4. Convert the first chunk into an embedding
vector = embeddings.embed_query(chunks[0].page_content)


# 5. Display embedding information
print(f"Embedding dimension: {len(vector)}")
print(f"First 10 values: {vector[:10]}")