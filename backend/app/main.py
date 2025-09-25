import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from backend.utils.RAG import add_document, query_data
from backend.utils.validators import validators

# Carrega variáveis de ambiente do arquivo .env
load_dotenv() 
os.getenv("GOOGLE_API_KEY")

app = FastAPI()

# Middleware para permitir requisições CORS (necessário para integração com frontend React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração da pasta do frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Caminho para armazenar PDFs localmente
LOCAL_PDF_STORAGE_DIR = "backend/utils/RAG/data"


@app.get("/", response_class=FileResponse, tags=["Frontend"])
def root():
    """
    Retorna o arquivo `index.html` do frontend.
    Essa rota serve a aplicação React no caminho raiz `/`.
    """
    return FileResponse(os.path.join("frontend", "index.html"))


@app.post("/save-pdf", tags=["Materiais"])
async def save_pdf(file: UploadFile = File(...)):
    """
    **Upload de PDF**

    Faz o upload de um arquivo PDF para o servidor e salva no diretório local.

    - **Parâmetros**:
        - `file`: Arquivo enviado (PDF)

    - **Respostas**:
        - `200 OK`: Arquivo salvo com sucesso
        - `400 Bad Request`: Arquivo inexistente | Tipo de arquivo não permitido
        - `500 Internal Server Error`: Erro interno ao salvar

    - **Exemplo de resposta**:
    ```json
    {
      "message": "Arquivo salvo localmente com sucesso!",
      "file_path": "backend/utils/RAG/data/exemplo.pdf",
      "created_data_directory": False (se backend/utils/data existir) | True (se backend/utils/data não existir)
    }
    ```
    """
    if not file:
        raise HTTPException(status_code=400, detail="Adicione um arquivo.")

    if not (file.filename.endswith(".pdf") or file.filename.endswith(".md")):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF ou Markdown são permitidos.")
    
    created_data_directory = False
    if not os.path.exists(LOCAL_PDF_STORAGE_DIR):
        os.makedirs(LOCAL_PDF_STORAGE_DIR)
        created_data_directory = True
        print(f"Diretório '{LOCAL_PDF_STORAGE_DIR}' criado.")

    file_path = os.path.join(LOCAL_PDF_STORAGE_DIR, file.filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        print(f"Arquivo '{file.filename}' salvo localmente em: {file_path}")
        return JSONResponse(status_code=200, content={
            "message": "Arquivo salvo localmente com sucesso!",
            "file_path": file_path,
            "created_data_directory": created_data_directory
        })
    except Exception as e:
        print(f"Erro ao salvar arquivo localmente: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")


@app.post("/process-pdf", tags=["Materiais"])
async def process_pdf(request: Request):
    """
    **Processar material com RAG**

    Processa o conteúdo de um PDF salvo e adiciona ao banco vetorial.

    - **Parâmetros** (JSON body):
        - `file_path`: Caminho do arquivo no servidor.

    - **Respostas**:
        - `200 OK`: Documento processado
        - `400 Bad Request`: Arquivo não encontrado
        - `500 Internal Server Error`: Erro ao processar

     - **Exemplo de resposta**:
    ```json
    {
      "message": "Documento processado com sucesso!"
    }
    ```
    """
    data = await request.json()
    file_path = data.get("file_path")
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Arquivo não encontrado.")
    
    try:    
        add_document.add_document(file_path)
        return JSONResponse(status_code=200, content={
            "message": "Documento processado com sucesso!",
        })
    except Exception as e:
        print(f"Erro ao processar arquivo localmente: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")


@app.post("/chat", tags=["Chat"])
async def chat(request: Request):
    """
    **Chat com RAG**

    Permite enviar uma pergunta ao modelo que consulta o banco vetorial
    dos materiais processados.

    - **Parâmetros** (JSON body):
        - `query`: Texto da pergunta.

    - **Respostas**:
        - `200 OK`: Retorna a resposta do RAG
        - `400 Bad Request`: Query não fornecida
        - `500 Internal Server Error`: Erro no processamento

    - **Exemplo de resposta**:
    ```json
    {
      "response": Resposta encontrada pelo RAG
    }
    ```
    """
    data = await request.json()
    query_text = data.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="Query não fornecida.")
    try:
        response = query_data.query(query_text)
        return JSONResponse(status_code=200, content={
            "response": response,
        })
    except Exception as e:
        print(f"Erro no chat: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")