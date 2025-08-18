from __future__ import annotations

import re
from typing import Annotated, Optional
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    StringConstraints,
    field_validator,
)

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class ViewFleetDTO(BaseModel):
    id: Annotated[int, Field(ge=1, description="ID del administrador (>= 1).")]
    

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
            }
        },
    )

class CreateBenefitsDTO(BaseModel):
    name: NonEmptyStr = Field(description="Nombre de la flotilla.")
    description: Optional[str] = Field(default=None, description="Descripción opcional de la flotilla.")
    points: Decimal = Field(description="Puntos como número decimal.")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Combustible",
                "description": "",
                "points": 100
            }
        },
    )

class UpdateBenefitsDTO(BaseModel):
    name: NonEmptyStr = Field(description="Nombre de la flotilla.")
    description: Optional[str] = Field(default=None, description="Descripción opcional de la flotilla.")
    points: Decimal = Field(description="Puntos como número decimal.")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Combustible",
                "description": "Cobertura ampliada",
                "points": 1500.00
            }
        },
    )