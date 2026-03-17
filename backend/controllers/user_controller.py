from fastapi import HTTPException
from models.user_models import GetUserRequest
from services.user_service import UserService

class UserController:

    @staticmethod
    def get_user_information(data: GetUserRequest):
        try:
            return UserService.get_user_information(user_id=data.user_id)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )