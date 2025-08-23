from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os, shutil

CHROMA_PATH = "RAG/chroma"

def create_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    Chroma(
        collection_name="vector_db",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )
    print("Sucessfully created a collection.")

create_database()