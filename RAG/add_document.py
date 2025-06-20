from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from uuid import uuid4

DATA_PATH = "RAG/data"
CHROMA_PATH = "RAG/chroma"

def load_document(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    return documents

def text_split(document):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=300,
        length_function=len,
        add_start_index=True,
        separators=["\n\n", "\n", " ", "##"]
    )

    chunks = text_splitter.split_documents(document)
    print(f"Total chunks: {len(chunks)}")

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
    
    document = load_document(file_path)
    chunks = text_split(document)
    documents = []

    for chunk in chunks:
        doc = Document(
            page_content=chunk.page_content,
            meta_data={"school_id": 1, "document_id": 1, "source": chunk.metadata["source"]}
        )
        documents.append(doc)

    uuids = [str(uuid4()) for _ in range(len(documents))]
    db.add_documents(documents=documents, ids=uuids)
    print("Sucessfully added document.")