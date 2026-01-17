from pydantic import BaseModel, Field
from typing import Literal

class GradeDocuments(BaseModel):
    binary_grade: Literal["yes", "no"] = Field(
        description="Pontuação de relevância: 'yes' se relevante, ou 'no' se não relevante"
    )