from langchain.messages import HumanMessage
from ai.models.models import gemini_25_flash
from ai.tools.retriever import retrieve
from ai.tools.multi_retriever import multi_retrieve
from ai.prompts.rewrite import REWRITE_PROMPT
from ai.prompts.generate import GENERATE_PROMPT

def generate_query_or_respond(state):
    response = gemini_25_flash.bind_tools([retrieve, multi_retrieve]).invoke(state["messages"])
    return {"messages": [response]}

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