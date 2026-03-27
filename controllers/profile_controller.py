from fastapi import HTTPException
from models.profile_models import CreateProfileRequest
from services.profile_service import ProfileService

class ProfileController:

    @staticmethod
    def create_profile(data: CreateProfileRequest):
        try:
            return ProfileService.create_profile(
                user_id=data.user_id, 
                name=data.name, 
                role=data.role, 
                class_ids=data.class_ids
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )