
from __future__ import annotations
from helpers.response import ExceptionResponse

from typing import List, Annotated
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, model_validator, StringConstraints

NonEmptyStr = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
PhoneStr    = Annotated[str, StringConstraints(pattern=r"^\+?\d[\d\s\-]{6,20}$")]
PlateStr    = Annotated[str, StringConstraints(min_length=3, max_length=20, strip_whitespace=True)]
YearStr     = Annotated[str, StringConstraints(pattern=r"^\d{4}$")]  # "2024", "2025", etc.

__all__ = ["VehicleDTO", "ProspectDTO"]

# --------- Modelos DTO ----------
class VehicleDTO(BaseModel):
    id_vehicles: int = Field(..., gt=0)
    branch: NonEmptyStr
    year: YearStr
    number_plate: PlateStr


class ProspectDTO(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    fullname: NonEmptyStr
    email: EmailStr
    phone: PhoneStr

    property_vehicle: bool
    property_vehicle_second: bool

    vehicles: List[VehicleDTO] = Field(default_factory=list)

    @model_validator(mode="after")
    def _require_vehicles_when_both_true(self) -> "ProspectDTO":
        if self.property_vehicle or self.property_vehicle_second:
            if not self.vehicles:
                raise ExceptionResponse(
                    error=['error_empty_vehicle']
                )
                
        return self

    @field_validator("phone")
    @classmethod
    def _normalize_phone(cls, v: str) -> str:
        return v.replace(" ", "").replace("-", "")
