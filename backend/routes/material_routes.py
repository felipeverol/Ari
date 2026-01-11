from fastapi import APIRouter, UploadFile, Depends, Form
from models.material_models import UploadMaterialRequest
from controllers.material_controller import MaterialController
from dependencies.permissions import require_teacher_in_class, require_role
from models.profile_models import ProfileRole

router = APIRouter(tags=["materials"])

@router.post("/upload")
async def upload_material(
    file: UploadFile, 
    class_id: str = Form(...),
    title: str = Form(...),
    _ = Depends(require_teacher_in_class), 
):
    data = UploadMaterialRequest(
        class_id=class_id,
        title=title
    )
    return await MaterialController.upload_material(file, data)