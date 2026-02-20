from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from ai.graph.nodes import (
    generate_query_or_respond,
    rerank_documents,
    rewrite_question,
    generate_answer,
)
from ai.graph.conditions import grade_documents
from ai.tools.retriever import retrieve


def build_graph():
    workflow = StateGraph(MessagesState)

    # Nodes
    workflow.add_node(generate_query_or_respond)
    workflow.add_node(rerank_documents)
    workflow.add_node(
        "retrieval_tools",
        ToolNode([retrieve]),
    )
    workflow.add_node(rewrite_question)
    workflow.add_node(generate_answer)

    # Entry
    workflow.add_edge(START, "generate_query_or_respond")

    # Decide: responde direto OU chama tools
    workflow.add_conditional_edges(
        "generate_query_or_respond",
        tools_condition,
        {
            "tools": "retrieval_tools",
            END: END,
        },
    )

    # Após retrieval → rerank
    workflow.add_edge("retrieval_tools", "rerank_documents")

    # Após rerank → grade
    workflow.add_conditional_edges(
        "rerank_documents",
        grade_documents,
    )

    # Finalização
    workflow.add_edge("generate_answer", END)
    workflow.add_edge("rewrite_question", "generate_query_or_respond")

    return workflow.compile()


if __name__ == "__main__":
    graph = build_graph()
    png_bytes = graph.get_graph().draw_mermaid_png()

    with open("graph.png", "wb") as f:
        f.write(png_bytes)

    print("✅ Grafo salvo em graph.png")