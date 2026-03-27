from pydantic import BaseModel

class CreateClassRequest(BaseModel):
    school_id: str
    name: str
    description: str | None = None

class GetClassesRequest(BaseModel):
    user_id: str