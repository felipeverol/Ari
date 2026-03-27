from pydantic import BaseModel

class CreateSchoolRequest(BaseModel):
    name: str
    address: str | None = None