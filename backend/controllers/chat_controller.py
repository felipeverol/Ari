from services.chat_service import ChatService
from models.chat_models import ChatRequest

class ChatController:
    @staticmethod
    async def chat(data: ChatRequest):
        response = await ChatService.chat(data.query, data.class_id)
        return {"response": response}