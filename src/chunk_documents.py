from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_PATH = "Data\Abhishek H B Resume.pdf"


# 1. Load PDF
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

print(f"Number of pages: {len(documents)}")


# 2. Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


# 3. Split documents into chunks
chunks = text_splitter.split_documents(documents)


# 4. Display results
print(f"Number of chunks: {len(chunks)}")

for i, chunk in enumerate(chunks[:5]):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk.page_content)
    print("Metadata:", chunk.metadata)