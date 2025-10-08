from __future__ import annotations
from typing import Annotated, Optional
import re
from pydantic import BaseModel, Field, ConfigDict, StringConstraints, field_validator, model_validator

NonEmptyStr = Annotated[str, StringConstraints(min_length=1, max_length=120)]
_SPACE_RE = re.compile(r"\s+")

class TypeMotorDTO(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        validate_assignment=True,
        populate_by_name=True
    )

    name: NonEmptyStr = Field(..., description="Nombre del recurso/proyecto.")

    @field_validator("name", mode="after")
    @classmethod
    def collapse_inner_spaces(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v:
            raise ValueError("value_cannot_be_empty")
        return _SPACE_RE.sub(" ", v)

    @model_validator(mode="after")
    def fill_defaults(self):
        # Si no vino 'model', usar el 'name'
        if self.model_ is None:
            self.model_ = self.name
        return self
