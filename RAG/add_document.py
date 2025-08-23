from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import MarkdownTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from uuid import uuid4
import pymupdf4llm

CHROMA_PATH = "RAG/chroma"
    
def load_and_text_split(file_path):
    md_text = pymupdf4llm.to_markdown(file_path)

    splitter = MarkdownTextSplitter(chunk_size=400, chunk_overlap=100)
    chunks = splitter.create_documents([md_text])

    return chunks

def add_document(file_path):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=embeddings
        )
    except Exception as e:
        print(f"Erro ao carregar o banco de dados: {e}")
        db = None
    
    chunks = load_and_text_split(file_path)

    for i, c in enumerate(chunks):
        print(f"\nChunk {i}: {c.page_content}")

    documents = []
    for chunk in chunks:
        doc = Document(
            page_content=chunk.page_content,
            meta_data={"school_id": 1, "document_id": 1}
        )
        documents.append(doc)

    uuids = [str(uuid4()) for _ in range(len(documents))]
    db.add_documents(documents=documents, ids=uuids)
    print("Sucessfully added document.")

if __name__ == "__main__":
    add_document("./RAG/data/Historia_da_Grecia_Antiga.pdf")