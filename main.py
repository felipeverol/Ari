# backend_rag/rag_service.py (Adicione este novo endpoint, mantenha o resto do código)

import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from RAG import add_document, query_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta a pasta 'frontend' para servir arquivos estáticos (JS, CSS, etc.)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Serve o index.html da pasta 'frontend' no root "/"
@app.get("/", response_class=FileResponse)
def root():
    return FileResponse(os.path.join("frontend", "teste.html"))

LOCAL_PDF_STORAGE_DIR = "RAG/data"

@app.post("/save-pdf")
async def save_pdf(file: UploadFile = File(...)):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".md")):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF ou Markdown são permitidos.")

    if not os.path.exists(LOCAL_PDF_STORAGE_DIR):
        os.makedirs(LOCAL_PDF_STORAGE_DIR)
        print(f"Diretório '{LOCAL_PDF_STORAGE_DIR}' criado.")

    unique_filename = file.filename
    file_path = os.path.join(LOCAL_PDF_STORAGE_DIR, unique_filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        print(f"Arquivo '{file.filename}' salvo localmente em: {file_path}")
        return JSONResponse(status_code=200, content={
            "message": "Arquivo salvo localmente com sucesso!",
            "file_path": file_path,
            "filename": unique_filename
        })
    except Exception as e:
        print(f"Erro ao salvar arquivo localmente: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")

@app.post("/process-pdf")
async def process_pdf(request: Request):
    data = await request.json()
    file_path = data.get("file_path")
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Arquivo não encontrado.")
    
    try:    
        add_document.add_document(file_path)
    except Exception as e:
        print(f"Erro ao processar arquivo localmente: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query_text = data.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="Query não fornecida.")
    try:
        response = query_data.query(query_text)
        return {"response": response}
    except Exception as e:
        print(f"Erro no chat: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")