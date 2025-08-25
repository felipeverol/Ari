from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from uuid import uuid4
from RAG import agentic_chunker as ac

CHROMA_PATH = "RAG/chroma"
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def load_and_split(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    text_splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type="gradient"
    )
    
    chunks = text_splitter.split_documents(docs)

    chunker = ac.AgenticChunker()
    chunker.add_propositions(chunks)
    chunker.pretty_print_chunks()
    chunker.pretty_print_chunk_outline()

    return chunks

def add_document(file_path):
    try:
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=embeddings
        )
    except Exception as e:
        print(f"Erro ao carregar o banco de dados: {e}")
        db = None
    
    chunks = load_and_split(file_path)

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