from langchain_core.tools import tool
from langchain_core.documents import Document
from typing import Annotated, List
from langchain_core.tools import InjectedToolArg
from langchain_core.runnables.config import RunnableConfig

from supabase_client import supabase
from ai.models.models import gemini_embedding_model

@tool(response_format="content_and_artifact")
def multi_retrieve(
    queries: List[str],
    config: Annotated[RunnableConfig, InjectedToolArg],
):
    """
    Retrieve and aggregate documents for multiple related queries (multi-hop retrieval).
    Use this tool when the user's question requires:
    - breaking the question into sub-queries,
    - gathering information from different documents,
    - or combining multiple pieces of context to produce a complete answer.
    """

    serialized_parts = []
    documents: List[Document] = []

    class_id = config.get("configurable", {}).get("class_id")
    if not class_id:
        raise ValueError("class_id não fornecido no config")

    for query in queries:
        query_embedding = gemini_embedding_model.embed_query(query)

        response = supabase.rpc(
            "match_material_chunk",
            {
                "query_embedding": query_embedding,
                "filter": {"class_id": class_id},
            }
        ).execute()

        rows = response.data or []

        docs = [
            Document(
                page_content=row["content"],
                metadata={
                    **(row.get("metadata") or {}),
                    "similarity": row["similarity"],
                    "query": query,  # 🔥 útil em multi-hop
                },
            )
            for row in rows
        ]

        documents.extend(docs)

        serialized_parts.append(
            "\n\n".join(
                f"Fonte: {doc.metadata}\nConteúdo: {doc.page_content}"
                for doc in docs
            )
        )

    serialized = "\n\n---\n\n".join(serialized_parts)

    return serialized, documents
