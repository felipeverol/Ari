# nodes.py
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from ai.models.models import gemini_25_flash, reranker
from ai.tools.retriever import retrieve
from ai.prompts.generate import GENERATE_PROMPT
from ai.prompts.system import SYSTEM_PROMPT
from supabase_client import supabase

N_MESSAGES = 10

# ── Utilitários ───────────────────────────────────────────────────────────────

def clean_history(messages: list, n: int) -> list:
    clean = [
        m for m in messages
        if isinstance(m, (HumanMessage, AIMessage))
        and not (isinstance(m, AIMessage) and m.tool_calls)
        and not isinstance(m, ToolMessage)
    ]
    return clean[-n:]

# ── Nós ───────────────────────────────────────────────────────────────────────

def generate_query_or_respond(state):
    system = SystemMessage(content=SYSTEM_PROMPT)
    history = clean_history(state["messages"], N_MESSAGES)
    response = gemini_25_flash.bind_tools([retrieve]).invoke(
        [system] + history
    )
    return {"messages": [response]}


def rerank_documents(state):
    messages = state["messages"]

    tool_call_msg = next(
        m for m in reversed(messages) if hasattr(m, "tool_calls") and m.tool_calls
    )
    queries = tool_call_msg.tool_calls[0]["args"]["queries"]
    question = queries[0] if len(queries) == 1 else "; ".join(queries)

    documents = messages[-1].artifact

    results = reranker.rerank(
        query=question,
        documents=[{"text": doc.page_content, **doc.metadata} for doc in documents],
        rank_fields=["text"],
        top_n=3,
    )

    top_docs = [documents[r["index"]] for r in results]
    context_text = "\n\n".join(doc.page_content for doc in top_docs)

    return {
        "retrieved_context": context_text,
        "retrieved_docs": top_docs
    }


def generate_answer(state):
    system = SystemMessage(content=GENERATE_PROMPT.format(context=state["retrieved_context"]))
    history = clean_history(state["messages"], N_MESSAGES)

    image_docs = [
        doc for doc in state.get("retrieved_docs", [])
        if doc.metadata.get("type") == "image" and doc.metadata.get("image_path")
    ]

    if image_docs:
        content = []
        for doc in image_docs:
            signed = supabase.storage.from_("materials").create_signed_url(
                path=doc.metadata["image_path"],
                expires_in=60
            )
            
            image_url = signed["signedUrl"]
            
            marker = f"[Imagem {doc.metadata.get('image_index')} da página {doc.metadata.get('page')}]"
            content.append({
                "type": "text", 
                "text": marker
            })
            content.append({
                "type": "image",
                "url": image_url
            })

        multimodal_message = HumanMessage(content=content)

        response = gemini_25_flash.invoke([system] + history + [multimodal_message])
    else:
        response = gemini_25_flash.invoke([system] + history)

    return {"messages": [response]}