from fastapi import APIRouter, UploadFile, File, Form
from models.material_models import UploadMaterialRequest
from controllers.material_controller import MaterialController

router = APIRouter()

@router.post("/upload")
async def upload_material(
    file: UploadFile = File(...),
    school_id: str = Form(...),
    class_id: str = Form(...),
    title: str = Form(...)
):
    data = UploadMaterialRequest(
        school_id=school_id,
        class_id=class_id,
        title=title
    )

    return await MaterialController.upload_material(file, data)
