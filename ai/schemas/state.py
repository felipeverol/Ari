from langgraph.graph import MessagesState
from langchain_core.documents import Document

class CustomState(MessagesState):
    retrieved_context: str
    retrieved_docs: list[Document]