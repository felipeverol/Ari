from fastapi import APIRouter, Depends
from controllers.auth_controller import AuthController
from models.auth_models import AuthRequest
from models.profile_models import ProfileRole
from dependencies.permissions import require_role

router = APIRouter(tags=["auth"])

@router.post("/signup")
def signup(
    data: AuthRequest,
    _ = Depends(require_role(ProfileRole.ADMIN))
):
    return AuthController.signup(data)

@router.post("/login")
def login(data: AuthRequest):
    return AuthController.login(data)
