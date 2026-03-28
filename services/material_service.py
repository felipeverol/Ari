import fitz
import uuid
import io
from PIL import Image
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from fastapi import UploadFile
from google import genai
from google.genai import types

from ai.models.models import gemini_embedding_model
from supabase_client import supabase

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
MIN_IMAGE_SIZE_BYTES = 5000
CONTEXT_CHARS = 300


class MaterialService:

    @staticmethod
    async def upload_material(file: UploadFile, class_id: str, title: str):
        try:
            file_content = await file.read()

            school_id = MaterialService.get_school_id(class_id=class_id)

            file_id, storage_path = await MaterialService.upload_to_storage(
                school_id=school_id,
                class_id=class_id,
                file=file,
                file_content=file_content
            )

            await MaterialService.create_material_record(
                file_id=file_id,
                class_id=class_id,
                title=title,
                storage_path=storage_path
            )

            chunks = MaterialService.extract_chunks_from_pdf(file_content)
            
            await MaterialService.store_embeddings(
                chunks=chunks,
                material_id=file_id,
                school_id=school_id,
                class_id=class_id
            )

            return {
                "material_id": file_id,
                "public_url": supabase.storage.from_("materials").get_public_url(storage_path)
            }

        except Exception as e:
            raise Exception(f"Erro no upload/processamento: {str(e)}")


    # ── Metadados ─────────────────────────────────────────────────────────────

    @staticmethod
    def get_school_id(class_id: str) -> str:
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
        return class_data["school_id"]

    @staticmethod
    async def upload_to_storage(school_id: str, class_id: str, file: UploadFile, file_content: bytes):
        file_id = str(uuid.uuid4())
        storage_path = f"{school_id}/{class_id}/{file_id}_{file.filename}"

        supabase.storage.from_("materials").upload(
            path=storage_path,
            file=file_content,
            file_options={"content-type": file.content_type}
        )

        return file_id, storage_path

    @staticmethod
    async def create_material_record(file_id: str, class_id: str, title: str, storage_path: str):
        supabase.table("material").insert({
            "id": file_id,
            "class_id": class_id,
            "title": title,
            "storage_path": storage_path
        }).execute()


    # ── Extração ──────────────────────────────────────────────────────────────

    @staticmethod
    def extract_blocks_from_page(page) -> list[dict]:
        blocks = []

        for block in page.get_text("blocks"):
            x0, y0, x1, y1, text, *_ = block
            if text.strip():
                blocks.append({"type": "text", "content": text.strip(), "y0": y0})

        for img in page.get_images(full=True):
            xref = img[0]
            img_bytes = page.parent.extract_image(xref)["image"]
            if len(img_bytes) < MIN_IMAGE_SIZE_BYTES:
                continue
            bbox = page.get_image_bbox(img)
            blocks.append({"type": "image", "content": img_bytes, "y0": bbox.y0})

        return sorted(blocks, key=lambda b: b["y0"])

    @staticmethod
    def extract_chunks_from_pdf(file_content: bytes) -> list[dict]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        doc = fitz.open(stream=file_content, filetype="pdf")
        all_chunks = []

        for page in doc:
            page_num = page.number + 1
            blocks = MaterialService.extract_blocks_from_page(page)

            text_buffer: list[str] = []
            buffer_size = 0

            def flush_buffer():
                nonlocal buffer_size
                if text_buffer:
                    all_chunks.append({
                        "type": "text",
                        "content": " ".join(text_buffer),
                        "page": page_num
                    })
                    text_buffer.clear()
                    buffer_size = 0

            image_counter = 1
            for i, block in enumerate(blocks):
                if block["type"] == "text":
                    if len(block["content"]) > CHUNK_SIZE * 2:
                        for sub in splitter.split_text(block["content"]):
                            text_buffer.append(sub)
                            buffer_size += len(sub)
                    else:
                        text_buffer.append(block["content"])
                        buffer_size += len(block["content"])

                    if buffer_size >= CHUNK_SIZE:
                        flush_buffer()

                elif block["type"] == "image":
                    context_before = " ".join(text_buffer)[-CONTEXT_CHARS:] if text_buffer else ""
                    context_after = next(
                        (b["content"][:CONTEXT_CHARS] for b in blocks[i+1:] if b["type"] == "text"), ""
                    )

                    flush_buffer()

                    all_chunks.append({
                        "type": "image",
                        "image_bytes": block["content"],
                        "image_index": image_counter,
                        "context_before": context_before,
                        "context_after": context_after,
                        "page": page_num
                    })

                    image_counter += 1

            flush_buffer()

        return all_chunks


    # ── Embeddings ────────────────────────────────────────────────────────────

    """
    
    Por enquanto, Langchain ainda não suporta modelos de embedding multimodal.
    Por isso, estamos usando o SDK oficial do Google.
    TODO: mudar para Langchain quando houver suporte.
    
    """

    @staticmethod
    def embed_image_chunk(chunk: dict) -> list[float]:
        client = genai.Client()
        
        result = client.models.embed_content(
            model="gemini-embedding-2-preview",
            contents=[
                types.Content(
                    parts=[
                        types.Part(text=chunk["context_before"]),
                        types.Part.from_bytes(
                            data=chunk["image_bytes"],
                            mime_type="image/png"
                        ),
                        types.Part(text=chunk["context_after"]),
                    ]
                )
            ]
        )
        return result.embeddings[0].values

    @staticmethod
    def upload_image_to_storage(image_bytes: bytes, school_id: str, class_id: str, material_id: str) -> str:
        image_id = str(uuid.uuid4())
        image_path = f"{school_id}/{class_id}/{material_id}/images/{image_id}.png"
        supabase.storage.from_("materials").upload(
            path=image_path,
            file=image_bytes,
            file_options={"content-type": "image/png"}
        )
        return supabase.storage.from_("materials").get_public_url(image_path)

    @staticmethod
    async def store_embeddings(chunks: list[dict], material_id: str, school_id: str, class_id: str):
        text_chunks = [c for c in chunks if c["type"] == "text"]
        image_chunks = [c for c in chunks if c["type"] == "image"]

        rows = []

        if text_chunks:
            contents = [c["content"] for c in text_chunks]
            embeddings = gemini_embedding_model.embed_documents(contents)
            for chunk, embedding in zip(text_chunks, embeddings):
                rows.append({
                    "material_id": material_id,
                    "content": chunk["content"],
                    "embedding": embedding,
                    "metadata": {"page": chunk["page"], "type": "text"}
                })

        contador = 0
        for chunk in image_chunks:
            contador += 1
            image_url = MaterialService.upload_image_to_storage(
                image_bytes=chunk["image_bytes"],
                school_id=school_id,
                class_id=class_id,
                material_id=material_id
            )
            print(f"{contador} imagem processada")
            embedding = MaterialService.embed_image_chunk(chunk)
            rows.append({
                "material_id": material_id,
                "content": f"{chunk['context_before']}\n[Imagem {chunk['image_index']} da página {chunk['page']}]\n{chunk['context_after']}",
                "embedding": embedding,
                "metadata": {
                    "page": chunk["page"],
                    "type": "image",
                    "image_url": image_url
                }
            })

        return supabase.table("material_chunk").insert(rows).execute()