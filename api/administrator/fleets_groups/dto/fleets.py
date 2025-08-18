from __future__ import annotations

import re
from typing import Annotated
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

class CreateFleetDTO(BaseModel):
    administrator_id: Annotated[int, Field(ge=1, description="ID del administrador (>= 1).")]
    name_contact: NonEmptyStr = Field(description="Nombre del contacto de la flotilla.")
    phone: NonEmptyStr = Field(description="Teléfono en formato E.164. Se normaliza automáticamente.")
    email: EmailStr = Field(description="Correo electrónico válido.")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "administrator_id": 1,
                "name_contact": "Test Flotilla 1",
                "phone": "+521 3322238886",
                "email": "test.flotilla@test.com",
            }
        },
    )
    

    @field_validator("phone", mode="before")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        """
        Quita espacios, guiones y paréntesis. Si no inicia con '+', lo agrega.
        Valida longitud E.164 (máx. 15 dígitos).
        """
        if not isinstance(v, str):
            raise TypeError("phone debe ser una cadena")

        # Mantener solo dígitos y '+'
        cleaned = re.sub(r"[^\d+]", "", v.strip())

        # Si no empieza con '+', lo agregamos
        if cleaned and not cleaned.startswith("+"):
            # Soportar prefijo '00' → '+'
            if cleaned.startswith("00"):
                cleaned = "+" + cleaned[2:]
            else:
                cleaned = "+" + cleaned

        # Validación simple E.164: + y 8–16 total (incluyendo '+'), con 1–15 dígitos después de '+'
        if not re.fullmatch(r"\+[1-9]\d{7,14}", cleaned):
            raise ValueError("phone no cumple con formato E.164 (ej: +5213322238886)")

        return cleaned
    
class UpdateFleetDTO(BaseModel):
    administrator_id: Annotated[int, Field(ge=1, description="ID del administrador (>= 1).")]
    name_contact: NonEmptyStr = Field(description="Nombre del contacto de la flotilla.")
    phone: NonEmptyStr = Field(description="Teléfono en formato E.164. Se normaliza automáticamente.")
    email: EmailStr = Field(description="Correo electrónico válido.")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "administrator_id": 1,
                "name_contact": "Test Flotilla 1",
                "phone": "+521 3322238886",
                "email": "test.flotilla@test.com",
            }
        },
    )

    @field_validator("phone", mode="before")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        """
        Quita espacios, guiones y paréntesis. Si no inicia con '+', lo agrega.
        Valida longitud E.164 (máx. 15 dígitos).
        """
        if not isinstance(v, str):
            raise TypeError("phone debe ser una cadena")

        # Mantener solo dígitos y '+'
        cleaned = re.sub(r"[^\d+]", "", v.strip())

        # Si no empieza con '+', lo agregamos
        if cleaned and not cleaned.startswith("+"):
            # Soportar prefijo '00' → '+'
            if cleaned.startswith("00"):
                cleaned = "+" + cleaned[2:]
            else:
                cleaned = "+" + cleaned

        # Validación simple E.164: + y 8–16 total (incluyendo '+'), con 1–15 dígitos después de '+'
        if not re.fullmatch(r"\+[1-9]\d{7,14}", cleaned):
            raise ValueError("phone no cumple con formato E.164 (ej: +5213322238886)")

        return cleaned