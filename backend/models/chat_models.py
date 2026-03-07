from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    class_id: str
    student_id: str