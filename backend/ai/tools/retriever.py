from langchain_core.tools import tool
from langchain_core.documents import Document
from typing import Annotated, List
from langchain_core.tools import InjectedToolArg
from langchain_core.runnables.config import RunnableConfig

from supabase_client import supabase
from ai.models.models import gemini_embedding_model

def apply_rrf(documents: List[Document], k=60):
    # Usamos o conteúdo como chave única para desduplicação
    doc_scores = {}
    content_to_doc = {}

    # 1. Ranking por Similaridade (Vetor)
    docs_by_similarity = sorted(documents, key=lambda d: d.metadata.get("similarity", 0), reverse=True)
    for rank, doc in enumerate(docs_by_similarity, 1):
        content = doc.page_content
        doc_scores[content] = doc_scores.get(content, 0) + (1.0 / (k + rank))
        content_to_doc[content] = doc

    # 2. Ranking por Sparse Score (Texto)
    docs_by_fts = [d for d in documents if (d.metadata.get("sparse_score") or 0) > 0.01]
    docs_by_fts = sorted(docs_by_fts, key=lambda d: d.metadata.get("sparse_score", 0), reverse=True)
    
    for rank, doc in enumerate(docs_by_fts, 1):
        content = doc.page_content
        doc_scores[content] = doc_scores.get(content, 0) + (1.0 / (k + rank))
        # O doc_map garante que preservamos o objeto Document original
        if content not in content_to_doc:
            content_to_doc[content] = doc

    # 3. Gerar lista final ordenada pelo novo Hybrid Score
    final_docs = []
    sorted_items = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    
    for content, score in sorted_items:
        doc = content_to_doc[content]
        doc.metadata["hybrid_score"] = score
        final_docs.append(doc)
        
    return final_docs

@tool(response_format="content_and_artifact")
def retrieve(
    queries: List[str],
    config: Annotated[RunnableConfig, InjectedToolArg],
):
    """
    Use this tool to retrieve relevant documents from the class materials.
    Provide one query for simple questions.
    Provide multiple queries when the question involves multiple concepts,
    entities, or aspects that should be searched separately.
    """
    
    all_docs_from_all_queries: List[Document] = []

    class_id = config.get("configurable", {}).get("class_id")
    if not class_id:
        raise ValueError("class_id não fornecido no config")

    for query in queries:
        query_embedding = gemini_embedding_model.embed_query(query)

        embeddings_response = supabase.rpc(
            "match_material_chunk_embeddings",
            {
                "content": query,
                "query_embedding": query_embedding,
                "filter": {"class_id": class_id},
                "match_count": 20 
            }
        ).execute()

        fts_response = supabase.rpc(
            "match_material_chunk_fts",
            {
                "content": query,
                "query_embedding": query_embedding,
                "filter": {"class_id": class_id},
                "match_count": 20 
            }
        ).execute()

        rows = embeddings_response.data + fts_response.data

        for row in rows:
            all_docs_from_all_queries.append(
                Document(
                    page_content=row["content"],
                    metadata={
                        **(row.get("metadata") or {}),
                        "similarity": row["similarity"],
                        "sparse_score": row.get("sparse_score"),
                        "query": query,
                    },
                )
            )

    # Aplica o RRF uma única vez em TUDO o que foi encontrado
    final_selection = apply_rrf(all_docs_from_all_queries)
    
    serialized = "\n\n---\n\n".join(
        f"Fonte: {doc.metadata}\nConteúdo: {doc.page_content}"
        for doc in final_selection
    )

    return serialized, final_selection