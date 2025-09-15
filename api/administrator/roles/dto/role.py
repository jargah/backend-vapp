from __future__ import annotations
from typing import Any, Dict, Annotated
import re
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, StringConstraints

_PHONE_RE = re.compile(r"^\+?[0-9][0-9\s\-]{6,20}$")

Username = Annotated[str, StringConstraints(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9._-]+$")]
FirstName = Annotated[str, StringConstraints(min_length=1, max_length=100)]
LastName  = Annotated[str, StringConstraints(min_length=1, max_length=120)]
PhoneStr  = Annotated[str, StringConstraints(min_length=7, max_length=25)]

class UserDTO(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={
            "examples": [
                {
                    "rol_id": 2,
                    "first_name": "Test",
                    "last_name": "Test 1",
                    "username": "test.test",
                    "email": "test@test.com",
                    "phone": "+52 333333333"
                }
            ],
            "description": "DTO para alta/edición de usuario básico.",
        }
    )

    rol_id: int = Field(..., ge=1, description="ID de rol (>=1).")
    first_name: FirstName
    last_name: LastName
    username: Username
    email: EmailStr
    phone: PhoneStr

    @field_validator("first_name", "last_name")
    @classmethod
    def non_empty_names(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("value_cannot_be_empty")
        return re.sub(r"\s+", " ", v.strip())

    @field_validator("username")
    @classmethod
    def normalize_username(cls, v: str) -> str:
        v = v.strip()
        if " " in v:
            raise ValueError("username_cannot_contain_spaces")
        return v.lower()

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: EmailStr) -> str:
        return str(v).lower()  # <- FIX

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = re.sub(r"\s+", " ", v.strip())
        if not _PHONE_RE.match(v):
            raise ValueError("invalid_phone_format")
        return v
