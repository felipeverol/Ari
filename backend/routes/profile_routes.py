from fastapi import APIRouter, Depends
from controllers.profile_controller import ProfileController
from models.auth_models import AuthRequest
from models.profile_models import ProfileRole, CreateProfileRequest
from dependencies.permissions import require_role

router = APIRouter(tags=["profile"])

@router.post("/create-profile")
def setup_profile(
    data: CreateProfileRequest,
    _ = Depends(require_role(ProfileRole.ADMIN))
):
    return ProfileController.create_profile(data)