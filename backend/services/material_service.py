from utils.ai.gemini_embedding import GeminiEmbeddingModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import UploadFile
import fitz
import uuid

from supabase_client import supabase

class MaterialService:

    @staticmethod
    async def upload_material(file: UploadFile, school_id: str, class_id: str, title: str):
        try:
            file_content = await file.read()

            file_id = str(uuid.uuid4())
            storage_path = f"/{school_id}/{class_id}/{file_id}_{file.filename}"

            response = supabase.storage.from_("materials").upload(
                storage_path,
                file_content,
                file_options={"content-type": file.content_type}
            )

            if "error" in response and response["error"] is not None:
                raise Exception("Erro ao fazer upload do arquivo")

            public_url = supabase.storage.from_("materials").get_public_url(storage_path)

            # 1) Create material record
            material_insert = supabase.table("material").insert({
                "id": file_id,
                "class_id": class_id,
                "title": title,
                "path": storage_path
            }).execute()

            # 2) Generate chunks and embeddings
            await MaterialService.process_material(
                file_bytes=file_content,
                material_id=file_id
            )

            return {
                "material_id": file_id,
                "storage_path": storage_path,
                "public_url": public_url,
            }

        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    async def process_material(file_bytes: bytes, material_id: str):

        # 1) Extract text from PDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text("text") + "\n"

        # 2) Chunking with LangChain
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )
        chunks = splitter.split_text(full_text)

        # 3) Embeddings with Gemini
        embedder = GeminiEmbeddingModel()

        # 4) Insert chunks + embeddings
        for index, chunk in enumerate(chunks):
            embedding = await embedder.embed(chunk)

            supabase.table("material_chunk").insert({
                "material_id": material_id,
                "chunk_index": index,
                "chunk_text": chunk,
                "embedding": embedding
            }).execute()

        return {"chunks": len(chunks)}
