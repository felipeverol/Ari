from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from uuid import uuid4

# Caminho para os dados de entrada e para o banco Chroma
DATA_PATH = "backend/utils/RAG/data"
CHROMA_PATH = "backend/utils/RAG/chroma"

def load_document(file_path):
    """
    Carrega um documento PDF e o converte em uma lista de Document objects do LangChain.

    Args:
        file_path (str): Caminho para o arquivo PDF.

    Returns:
        list[Document]: Lista de documentos carregados.
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    return documents

def text_split(document):
    """
    Divide um documento em chunks menores, respeitando limites de tamanho e sobreposição.

    Args:
        document (list[Document]): Lista de documentos carregados.

    Returns:
        list[Document]: Lista de chunks gerados.
    """
    text_splitter = RecursiveCharacterTextSplitter( # TODO: ajustar o chunking para otimizar o RAG
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
        separators = ["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(document)

    return chunks


def add_document(file_path):
    """
    Adiciona um documento PDF ao banco vetorial persistido no Chroma.

    Etapas:
    - Conecta ao banco persistido em CHROMA_PATH.
    - Carrega e divide o documento em chunks.
    - Cria objetos Document com metadados (school_id, document_id, source).
    - Gera IDs únicos para cada chunk.
    - Insere os documentos no banco.

    Args:
        file_path (str): Caminho para o arquivo PDF a ser adicionado.
    """
    try:
        # Inicializa embeddings e conecta ao banco
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=embeddings
        )
    except Exception as e:
        print(f"Erro ao carregar o banco de dados: {e}")
        return
    
    # Carregar e dividir documento
    document = load_document(file_path)
    chunks = text_split(document)
    
    documents = []
    for chunk in chunks:
        doc = Document(
            page_content=chunk.page_content,
            metadata={"school_id": 1, "document_id": 1, "source": chunk.metadata["source"]} # TODO: ajustar metadados
        )
        documents.append(doc)

    # Gerar UUIDs únicos para cada chunk
    uuids = [str(uuid4()) for _ in range(len(documents))]
    
    # Inserir no banco
    db.add_documents(documents=documents, ids=uuids)
    print("Sucessfully added document.")