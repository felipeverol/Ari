import fitz
import uuid
from typing import List, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from fastapi import UploadFile

from ai.models.models import gemini_embedding_model
from supabase_client import supabase

class MaterialService:
    
    @staticmethod
    async def upload_material(file: UploadFile, class_id: str, title: str):
        try:
            file_content = await file.read()

            # 1. Busca metadados da escola (Isolamento)
            class_data = supabase.table("class").select("school_id").eq("id", class_id).single().execute().data
            if not class_data:
                raise Exception("Turma não encontrada")
            school_id = class_data["school_id"]

            # 2. Upload para Storage
            file_id = str(uuid.uuid4())
            storage_path = f"{school_id}/{class_id}/{file_id}_{file.filename}"
            
            supabase.storage.from_("materials").upload(
                path=storage_path,
                file=file_content,
                file_options={"content-type": file.content_type}
            )

            # 3. Registro no Banco de Dados
            supabase.table("material").insert({
                "id": file_id,
                "class_id": class_id,
                "title": title,
                "storage_path": storage_path
            }).execute()

            # 4. Processamento em Cadeia
            pages = MaterialService.extract_text_from_pdf(file_content)
            documents = MaterialService.chunk_text(pages, material_id=file_id, school_id=school_id, class_id=class_id)
            await MaterialService.store_embeddings(documents, material_id=file_id)

            return {
                "material_id": file_id,
                "public_url": supabase.storage.from_("materials").get_public_url(storage_path)
            }
        except Exception as e:
            raise Exception(f"Erro no upload/processamento: {str(e)}")

    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> List[Tuple[int, str]]:
        """Extrai texto por página para manter rastreabilidade."""
        doc = fitz.open(stream=file_content, filetype="pdf")
        return [(page.number + 1, page.get_text("text")) for page in doc]

    @staticmethod
    def chunk_text(pages: List[Tuple[int, str]], material_id: str, school_id: str, class_id: str) -> List[Document]:
        """Divide o texto e injeta metadados de segurança (Multitenancy)."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        documents = []

        for page_num, text in pages:
            chunks = splitter.split_text(text)
            for chunk in chunks:
                # O segredo do isolamento está aqui: school_id e class_id no metadado
                documents.append(Document(
                    page_content=chunk,
                    metadata={
                        "page": page_num
                    }
                ))
        return documents

    @staticmethod
    async def store_embeddings(documents: List[Document], material_id: str):
        """Gera embeddings e salva no pgvector do Supabase."""
        contents = [doc.page_content for doc in documents]
        embeddings = gemini_embedding_model.embed_documents(contents)

        rows = []
        for doc, embedding in zip(documents, embeddings):
            rows.append({
                "material_id": material_id,
                "content": doc.page_content,
                "embedding": embedding,
                "metadata": doc.metadata # Inclui school_id e class_id
            })

        return supabase.table("material_chunk").insert(rows).execute()