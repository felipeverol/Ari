from fastapi import APIRouter, Depends
from controllers.class_controller import ClassController
from models.class_models import CreateClassRequest
from dependencies.permissions import require_role
from models.profile_models import ProfileRole

router = APIRouter(tags=["class"])

@router.post("/class")
def create_class(
    data: CreateClassRequest,
    _ = Depends(require_role(ProfileRole.ADMIN)),
):
    return ClassController.create_class(data)