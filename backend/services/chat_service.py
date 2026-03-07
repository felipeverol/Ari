from langchain_core.messages import AIMessage, HumanMessage
from ai.graph.builder import build_graph
from supabase_client import supabase

class ChatService:
    graph = build_graph()

    @staticmethod
    async def stream(query: str, class_id: str, student_id: str):
        conversation_id = ChatService.get_or_create_conversation(student_id, class_id)
        thread_id = f"{class_id}:{student_id}"

        config = {
            "configurable": {
                "thread_id": thread_id,
                "class_id": class_id
            }
        }

        full_response = []

        async for event in ChatService.graph.astream_events(
            {"messages": [HumanMessage(content=query)]},
            config=config,
            version="v2"
        ):
            if event["event"] == "on_chat_model_stream" and event["metadata"].get("langgraph_node") in (
                "generate_answer",
                "generate_query_or_respond",
            ):
                chunk = event["data"]["chunk"].content
                if chunk:
                    if isinstance(chunk, list):
                        chunk = "".join(c.get("text", "") for c in chunk if isinstance(c, dict))
                    if chunk:
                        full_response.append(chunk)
                        yield f"data: {chunk}\n\n"

        # Salva no banco apenas após o streaming completo
        full_content = "".join(full_response)
        ChatService.save_message(conversation_id, "user", query)
        ChatService.save_message(conversation_id, "assistant", full_content)

        yield "data: [DONE]\n\n"

    @staticmethod
    def get_or_create_conversation(student_id: str, class_id: str) -> str:
        result = (
            supabase
            .table("conversation")
            .select("id")
            .eq("student_id", student_id)
            .eq("class_id", class_id)
            .limit(1)
            .execute()
        )

        if result.data:
            return result.data[0]["id"]

        conversation = (
            supabase
            .table("conversation")
            .insert({
                "student_id": student_id,
                "class_id": class_id
            })
            .execute()
        )

        return conversation.data[0]["id"]

    @staticmethod
    def save_message(conversation_id: str, role: str, content: str):
        (
            supabase
            .table("message")
            .insert({
                "conversation_id": conversation_id,
                "role": role,
                "content": content
            })
            .execute()
        )