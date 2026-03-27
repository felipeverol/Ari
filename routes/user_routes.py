from fastapi import APIRouter, Depends
from controllers.user_controller import UserController
from models.user_models import GetUserRequest
from dependencies.auth import get_current_user

router = APIRouter(tags=["user"])

@router.get("/")
def get_user_information(
    user = Depends(get_current_user)
):
    return UserController.get_user_information(GetUserRequest(user_id=user.id))