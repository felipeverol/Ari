from fastapi import APIRouter, Depends
from controllers.auth_controller import AuthController
from models.auth_models import LoginRequest, SignUpRequest
from models.profile_models import ProfileRole
from dependencies.permissions import require_role

router = APIRouter(tags=["auth"])

@router.post("/signup")
def signup(data: SignUpRequest, _ = Depends(require_role(ProfileRole.ADMIN))):
    return AuthController.signup(data)

@router.post("/login")
def login(body: LoginRequest):
    return AuthController.login(body)
