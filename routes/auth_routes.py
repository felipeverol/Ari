from fastapi import APIRouter, Depends
from controllers.auth_controller import AuthController
from models.auth_models import SignupRequest, LoginRequest
from models.profile_models import ProfileRole
from dependencies.permissions import require_role

router = APIRouter(tags=["auth"])

@router.post("/signup")
def signup(
    data: SignupRequest,
    _ = Depends(require_role(ProfileRole.ADMIN))
):
    return AuthController.signup(data)

@router.post("/login")
def login(data: LoginRequest):
    return AuthController.login(data)
