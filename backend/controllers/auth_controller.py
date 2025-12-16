from fastapi import HTTPException
from services.auth_service import AuthService
from models.auth_models import LoginRequest, SignUpRequest

class AuthController:
    
    @staticmethod
    def signup(data: SignUpRequest):
        try:
            return AuthService.signup(data.email, data.password)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def login(data: LoginRequest):
        try:
            return AuthService.login(data.email, data.password)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
