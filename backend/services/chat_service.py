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

        return result

        messages = result.get("messages", [])

        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and not msg.tool_calls:
                return msg.content

        raise ValueError("Nenhuma resposta final encontrada.")