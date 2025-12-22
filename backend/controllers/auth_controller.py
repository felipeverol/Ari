from fastapi import HTTPException
from services.auth_service import AuthService
from models.auth_models import AuthRequest

class AuthController:
    
    @staticmethod
    def signup(data: AuthRequest):
        try:
            return AuthService.signup(
                email=data.email,
                password=data.password
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    @staticmethod
    def login(data: AuthRequest):
        try:
            return AuthService.login(
                email=data.email,
                password=data.password
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
