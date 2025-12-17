from fastapi import APIRouter, Depends, Form
from controllers.class_controller import ClassController
from models.class_models import CreateClassRequest
from dependencies.permissions import require_role

router = APIRouter(tags=["class"])

@router.post("/class")
def create_class(
    data: CreateClassRequest,
    _ = Depends(require_role("admin")),
):
    return ClassController.create_class(data)