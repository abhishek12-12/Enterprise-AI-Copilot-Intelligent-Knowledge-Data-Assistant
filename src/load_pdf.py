from langchain_community.document_loaders import PyPDFLoader

PDF_PATH = "Data\Abhishek H B Resume.pdf"

loader = PyPDFLoader(PDF_PATH)

documents = loader.load()

print(f"Number of pages: {len(documents)}")

for i, document in enumerate(documents[:2]):
    print(f"\n--- Page {i + 1} ---")
    print(document.page_content[:1000])