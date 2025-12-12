from fastapi import HTTPException, UploadFile
from models.material_models import UploadMaterialRequest
from services.material_service import MaterialService

class MaterialController:

    @staticmethod
    async def upload_material(file: UploadFile, data: UploadMaterialRequest):
        try:
            return await MaterialService.upload_material(
                file=file,
                school_id=data.school_id,
                class_id=data.class_id,
                title=data.title
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))