from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os, shutil

# Caminho onde ficam os dados e o Chroma
DATA_PATH = "backend/utils/RAG/data"
CHROMA_PATH = "backend/utils/RAG/chroma"

def create_database():
    """
    Cria (ou recria) a base vetorial persistida no ChromaDB.

    Etapas:
    - Remove a pasta persistida existente em CHROMA_PATH, se ela já existir.
    - Inicializa embeddings usando o modelo "models/embedding-001".
    - Cria uma coleção no Chroma chamada "vector_db".
    - Persiste os metadados no diretório CHROMA_PATH.

    Observação:
    Esta função apenas inicializa a coleção vazia.
    """
    # Se já existe um banco, remove para criar do zero
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    # Definição do modelo de embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Inicialização da coleção vetorial
    Chroma(
        collection_name="vector_db",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )
    print("Sucessfully created a collection.")

if __name__ == "__main__":
    create_database()