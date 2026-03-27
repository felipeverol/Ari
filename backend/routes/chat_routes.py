from fastapi import APIRouter, Depends, Form
from fastapi.responses import StreamingResponse
from dependencies.permissions import require_student_in_class
from controllers.chat_controller import ChatController
from models.chat_models import ChatRequest

router = APIRouter(tags=["chat"])

@router.post("/")
async def chat(
    query: str = Form(...),
    class_id: str = Form(...),
    student = Depends(require_student_in_class)
):
    data = ChatRequest(
        query=query,
        class_id=class_id,
        student_id=student.id
    )
    return StreamingResponse(
        ChatController.stream(data),
        media_type="text/event-stream"
    )