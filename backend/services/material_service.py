import fitz
import uuid
import base64
from typing import List, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from fastapi import UploadFile

from ai.models.models import gemini_embedding_model, gemini_25_flash_lite
from supabase_client import supabase

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
MIN_IMAGE_SIZE_BYTES = 5000

class MaterialService:

    @staticmethod
    async def upload_material(file: UploadFile, class_id: str, title: str):
        try:
            file_content = await file.read()

            # 1. Busca metadados da escola
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

            # 2. Upload Storage
            file_id = str(uuid.uuid4())
            storage_path = f"{school_id}/{class_id}/{file_id}_{file.filename}"
            
            supabase.storage.from_("materials").upload(
                path=storage_path,
                file=file_content,
                file_options={"content-type": file.content_type}
            )
            
            # 3. Registro no banco
            supabase.table("material").insert({
                "id": file_id,
                "class_id": class_id,
                "title": title,
                "storage_path": storage_path
            }).execute()

            # 4. Extração, chunking e embeddings
            pages = MaterialService.extract_text_from_pdf(file_content)
            documents = MaterialService.chunk_text(pages)
            await MaterialService.store_embeddings(documents, material_id=file_id)

            return {
                "material_id": file_id,
                "public_url": supabase.storage.from_("materials").get_public_url(storage_path)
            }

        except Exception as e:
            raise Exception(f"Erro no upload/processamento: {str(e)}")


    # ── Extração ──────────────────────────────────────────────────────────────

    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> List[Tuple[int, str]]:
        doc = fitz.open(stream=file_content, filetype="pdf")
        pages_data = []

        for page in doc:
            page_text = page.get_text("text")

            image_descriptions = []
            for img_bytes in MaterialService.extract_images_from_page(page):
                if len(img_bytes) < MIN_IMAGE_SIZE_BYTES:
                    continue
                try:
                    description = MaterialService.describe_image(img_bytes)
                    print(description + "\n")
                    image_descriptions.append(f"\n[Descrição de imagem]\n{description}\n")
                except Exception:
                    continue

            full_text = page_text + "\n".join(image_descriptions)
            pages_data.append((page.number + 1, full_text))

        return pages_data

    @staticmethod
    def extract_images_from_page(page) -> List[bytes]:
        images = []
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = page.parent.extract_image(xref)
            images.append(base_image["image"])
        return images

    @staticmethod
    def describe_image(image_bytes: bytes) -> str:
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": (
                        "Descreva esta imagem de uma apostila educacional. "
                        "Explique o conceito representado e transcreva "
                        "qualquer texto visível."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{image_base64}"
                }
            ]
        )
        return gemini_25_flash_lite.invoke([message]).content


    # ── Chunking ──────────────────────────────────────────────────────────────

    @staticmethod
    def chunk_text(pages: List[Tuple[int, str]]) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        documents = []
        for page_num, text in pages:
            for chunk in splitter.split_text(text):
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={"page": page_num}
                    )
                )
        return documents


    # ── Embeddings ────────────────────────────────────────────────────────────

    @staticmethod
    async def store_embeddings(documents: List[Document], material_id: str):
        contents = [doc.page_content for doc in documents]
        embeddings = gemini_embedding_model.embed_documents(contents)

        rows = [
            {
                "material_id": material_id,
                "content": doc.page_content,
                "embedding": embedding,
                "metadata": doc.metadata
            }
            for doc, embedding in zip(documents, embeddings)
        ]

        return supabase.table("material_chunk").insert(rows).execute()