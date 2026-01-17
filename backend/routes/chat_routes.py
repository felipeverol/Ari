from fastapi import APIRouter, Depends, Form
from dependencies.permissions import require_student_in_class
from controllers.chat_controller import ChatController
from models.chat_models import ChatRequest

router = APIRouter(tags=["chat"])

@router.post("/chat")
async def chat(
    query: str = Form(...),
    class_id: str = Form(...),
    _ = Depends(require_student_in_class)
):
    data = ChatRequest(
        query=query,
        class_id=class_id
    )
    return await ChatController.chat(data)