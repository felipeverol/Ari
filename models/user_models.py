from pydantic import BaseModel

class GetUserRequest(BaseModel):
    user_id: str