from langgraph.graph import MessagesState

class CustomState(MessagesState):
    contextualized_question: str
    retrieved_context: str