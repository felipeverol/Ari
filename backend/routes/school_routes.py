from fastapi import APIRouter, Depends, Form
from controllers.school_controller import SchoolController
from models.school_models import CreateSchoolRequest
from dependencies.permissions import require_role

router = APIRouter(tags=["school"])

@router.post("/school")
def create_school(
    data: CreateSchoolRequest,
    _ = Depends(require_role("admin")),
):
    return SchoolController.create_school(data)