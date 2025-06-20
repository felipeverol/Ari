# backend_rag/rag_service.py (Adicione este novo endpoint, mantenha o resto do código)

import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique o domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta a pasta 'frontend' para servir arquivos estáticos (JS, CSS, etc.)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Serve o index.html da pasta 'frontend' no root "/"
@app.get("/", response_class=FileResponse)
def root():
    return FileResponse(os.path.join("frontend", "index.html"))

LOCAL_PDF_STORAGE_DIR = "RAG/data"

@app.post("/save-pdf")
async def save_local_pdf(file: UploadFile = File(...)):
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

# O resto dos seus endpoints, como /process-pdf e / (root), permanecem inalterados
# ...