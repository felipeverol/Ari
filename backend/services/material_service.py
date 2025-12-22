from ai.models.gemini_embedding import GeminiEmbeddingModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import UploadFile
import fitz
import uuid

from supabase_client import supabase

class MaterialService:

    @staticmethod
    async def upload_material(
        file: UploadFile,
        class_id: str,
        title: str
    ):
        try:
            file_content = await file.read()

            # TODO: modularizar, colocar no school_service
            # 1) Get school_id from class_id
            class_data = (
                supabase
                .table("class")
                .select("school_id")
                .eq("id", class_id)
                .single()
                .execute()
                .data
            )

            if not class_data:
                raise Exception("Turma não encontrada")

            school_id = class_data["school_id"]

            # 2) Upload file to Supabase Storage
            file_id = str(uuid.uuid4()) # TODO: aqui talvez seria melhor colocar uuid do supabase ?
            storage_path = f"/{school_id}/{class_id}/{file_id}_{file.filename}"

            supabase.storage.from_("materials").upload(
                path=storage_path,
                file=file_content,
                file_options={"content-type": file.content_type}
            )

            public_url = supabase.storage.from_("materials").get_public_url(storage_path)

            # 3) Insert material record in database
            supabase.table("material").insert({
                "id": file_id,
                "class_id": class_id,
                "title": title,
                "storage_path": storage_path
            }).execute()

            # 4) Process material: extract text, chunk, embed, store
            await MaterialService.process_material(
                file_content=file_content,
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
    async def process_material(file_content: bytes, material_id: str):

        # 1) Extract text from PDF
        doc = fitz.open(
            stream=file_content,
            filetype="pdf"
        )
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
        embeddings = embedder.embed_documents(chunks)

        # 4) Insert chunks + embeddings
        for index, chunk in enumerate(chunks):
            embedding = embeddings[index]

            supabase.table("material_chunk").insert({
                "material_id": material_id,
                "chunk_index": index,
                "chunk_text": chunk,
                "embedding": embedding
            }).execute()

        return {"chunks": len(chunks)}
