from fastapi import HTTPException
from models.school_models import CreateSchoolRequest
from services.school_service import SchoolService

class SchoolController:

    @staticmethod
    def create_school(data: CreateSchoolRequest):
        try:
            return SchoolService.create_school(
                name=data.name,
                address=data.address
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        

    