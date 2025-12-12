from fastapi import HTTPException
from services.auth_service import AuthService

class AuthController:
    
    @staticmethod
    def signup(data):
        try:
            return AuthService.signup(data.email, data.password)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def login(data):
        try:
            return AuthService.login(data.email, data.password)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
