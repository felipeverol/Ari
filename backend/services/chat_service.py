from langchain_core.messages import AIMessage
from ai.graph.builder import build_graph

class ChatService:
    graph = build_graph()

    @staticmethod
    async def chat(query: str, class_id: str) -> str:
        config = {
            "configurable": {
                "class_id": class_id
            }
        }
        
        result = ChatService.graph.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=config
        )

        for m in result["messages"]:
            m.pretty_print()
            
        last_message = result["messages"][-1]
        content = last_message.content
        
        if isinstance(content, list):
            return content[-1]["text"]

        return content