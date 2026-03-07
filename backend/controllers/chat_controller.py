from services.chat_service import ChatService
from models.chat_models import ChatRequest

class ChatController:
    @staticmethod
    async def stream(data: ChatRequest):
        async for chunk in ChatService.stream(data.query, data.class_id, data.student_id):
            yield chunk