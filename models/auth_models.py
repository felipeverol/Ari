from pydantic import BaseModel
from models.profile_models import ProfileRole

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    role: ProfileRole
    class_ids: list[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str