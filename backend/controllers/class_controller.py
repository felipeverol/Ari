from fastapi import HTTPException
from models.class_models import CreateClassRequest, GetClassesRequest
from services.class_service import ClassService

class ClassController:

    @staticmethod
    def create_class(data: CreateClassRequest):
        try:
            return ClassService.create_class(
                school_id=data.school_id,
                name=data.name,
                description=data.description
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        
    @staticmethod
    def get_classes(data: GetClassesRequest):
        try:
            return ClassService.get_classes(user_id=data.user_id)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )