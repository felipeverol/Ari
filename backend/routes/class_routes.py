from fastapi import APIRouter, Depends
from controllers.class_controller import ClassController
from models.class_models import CreateClassRequest, GetClassesRequest
from dependencies.permissions import require_role
from dependencies.auth import get_current_user
from models.profile_models import ProfileRole

router = APIRouter(tags=["class"])

@router.post("/")
def create_class(
    data: CreateClassRequest,
    _ = Depends(require_role(ProfileRole.ADMIN)),
):
    return ClassController.create_class(data)

@router.get("/")
def get_classes(
    user = Depends(get_current_user)
):
    return ClassController.get_classes(GetClassesRequest(user_id=user.id))