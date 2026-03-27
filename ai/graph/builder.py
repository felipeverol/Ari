# graph.py
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from ai.graph.nodes import (
    generate_query_or_respond,
    rerank_documents,
    generate_answer,
)
from ai.tools.retriever import retrieve
from ai.schemas.state import CustomState
from supabase_client import checkpointer

def build_graph():
    workflow = StateGraph(CustomState)

    workflow.add_node(generate_query_or_respond)
    workflow.add_node("retrieval_tools", ToolNode([retrieve]))
    workflow.add_node(rerank_documents)
    workflow.add_node(generate_answer)

    workflow.add_edge(START, "generate_query_or_respond")

    workflow.add_conditional_edges(
        "generate_query_or_respond",
        tools_condition,
        {
            "tools": "retrieval_tools",
            END: END,
        },
    )

    workflow.add_edge("retrieval_tools", "rerank_documents")
    workflow.add_edge("rerank_documents", "generate_answer")
    workflow.add_edge("generate_answer", END)

    return workflow.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    graph = build_graph()
    png_bytes = graph.get_graph().draw_mermaid_png()

    with open("ai/graph/graph.png", "wb") as f:
        f.write(png_bytes)

    print("✅ Grafo salvo em graph.png")