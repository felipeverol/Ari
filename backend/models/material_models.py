from pydantic import BaseModel

class UploadMaterialRequest(BaseModel):
    school_id: str
    class_id: str
    title: str
