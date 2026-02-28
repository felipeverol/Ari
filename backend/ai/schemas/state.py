from langgraph.graph import MessagesState

class CustomState(MessagesState):
    rewrite_count: int