from fastapi import APIRouter, Depends
from controllers.school_controller import SchoolController
from models.school_models import CreateSchoolRequest
from models.profile_models import ProfileRole
from dependencies.permissions import require_role

router = APIRouter(tags=["school"])

@router.post("/create-school")
def create_school(
    data: CreateSchoolRequest,
    _ = Depends(require_role(ProfileRole.ADMIN)),
):
    return SchoolController.create_school(data)