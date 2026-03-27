from pydantic import BaseModel
from typing import List
from enum import Enum

class ProfileRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    

class CreateProfileRequest(BaseModel):
    user_id: str
    name: str
    role: ProfileRole
    class_ids: List[str] = []