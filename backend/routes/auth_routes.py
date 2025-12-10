from fastapi import APIRouter
from controllers.auth_controller import AuthController
from models.auth_models import LoginRequest, SignUpRequest

router = APIRouter()

@router.post("/signup")
def signup(data: SignUpRequest):
    return AuthController.signup(data)

@router.post("/login")
def login_route(body: LoginRequest):
    return AuthController.login(body)
