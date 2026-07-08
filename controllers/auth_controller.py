from fastapi import HTTPException
from services.auth_service import AuthService
from models.auth_models import SignupRequest, LoginRequest

class AuthController:
    
    @staticmethod
    def signup(data: SignupRequest):
        try:
            return AuthService.signup(
                email=data.email,
                password=data.password,
                name=data.name,
                role=data.role,
                class_ids=data.class_ids
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    @staticmethod
    def login(data: LoginRequest):
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
