from fastapi import HTTPException
from models.class_models import CreateClassRequest
from services.class_service import ClassService

class ClassController:

    @staticmethod
    def create_class(data: CreateClassRequest):
        try:
            return ClassService.create_class(data.school_id, data.name, data.description)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))