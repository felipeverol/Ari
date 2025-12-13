from pydantic import BaseModel

class UploadMaterialRequest(BaseModel):
    class_id: str
    title: str