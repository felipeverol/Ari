from langchain.messages import HumanMessage
from ai.models.models import gemini_25_flash, reranker
from ai.tools.retriever import retrieve
from ai.prompts.rewrite import REWRITE_PROMPT
from ai.prompts.generate import GENERATE_PROMPT

def generate_query_or_respond(state):
    response = gemini_25_flash.bind_tools([retrieve]).invoke(state["messages"])
    return {"messages": [response]}

def rerank_documents(state):
    question = state["messages"][0].content
    documents = state["messages"][-1].artifact 

    rerank_input = [
        {
            "text": doc.page_content,
            "similarity": doc.metadata.get("similarity"),
            "query": doc.metadata.get("query"),
            **doc.metadata,
        }
        for doc in documents
    ]

    results = reranker.rerank(
        query=question,
        documents=rerank_input,
        rank_fields=["text"],
        top_n=3,
    )

    top_docs = [documents[r["index"]] for r in results]
    context = "\n\n".join(doc.page_content for doc in top_docs)

    return {"messages": [HumanMessage(content=context)]}

def rewrite_question(state):
    question = state["messages"][0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = gemini_25_flash.invoke([{"role": "user", "content": prompt}])
    return {"messages": [HumanMessage(content=response.content)]}

def generate_answer(state):
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = gemini_25_flash.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}