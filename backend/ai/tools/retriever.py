from langchain_core.tools import tool
from langchain_core.documents import Document
from typing import Annotated
from langchain_core.tools import InjectedToolArg
from langchain_core.runnables.config import RunnableConfig

from supabase_client import supabase
from ai.models.models import gemini_embedding_model


@tool(response_format="content_and_artifact")
def retrieve(query: str, config: Annotated[RunnableConfig, InjectedToolArg]):
    """Retrieve information related to a query."""

    class_id = config.get("configurable", {}).get("class_id")

    query_embedding = gemini_embedding_model.embed_query(query)

    response = supabase.rpc(
        "match_material_chunk",
        {
            "query_embedding": query_embedding,
            "filter" : {"class_id": class_id},
        }
    ).execute()

    rows = response.data or []

    documents = [
        Document(
            page_content=row["content"],
            metadata={
                **(row.get("metadata") or {}),
                "similarity": row["similarity"]
            }
        )
        for row in rows
    ]

    serialized = "\n\n".join(
        f"Fonte: {doc.metadata}\nConteúdo: {doc.page_content}"
        for doc in documents
    )

    return serialized, documents