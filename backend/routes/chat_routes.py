from fastapi import APIRouter
from controllers.chat_controller import ChatController
from models.chat_models import ChatRequest

router = APIRouter(tags=["chat"])

@router.post("/chat")
async def chat(data: ChatRequest):
    return await ChatController.chat(data)