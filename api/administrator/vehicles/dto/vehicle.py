from __future__ import annotations
from typing import Annotated
import re
from pydantic import BaseModel, Field, ConfigDict, StringConstraints, field_validator

# Tipos reutilizables
NonEmptyStr = Annotated[str, StringConstraints(min_length=1, max_length=120)]

_SPACE_RE = re.compile(r"\s+")

class VehicleDTO(BaseModel):
    """
    Esquema estricto para:
    {
        "name": "Test",
        "branch": "Test",
        "model": "Test"
    }
    Todos los campos son obligatorios.
    """
    model_config = ConfigDict(
        extra='forbid',                 # Rechazar claves desconocidas
        str_strip_whitespace=True,      # Recorta espacios a ambos lados
        validate_assignment=True,       # Revalida en asignaciones posteriores
        populate_by_name=True           # Permitir asignar por nombre de campo también
    )

    name: NonEmptyStr = Field(..., description="Nombre del recurso/proyecto.")
    branch: NonEmptyStr = Field(..., description="Rama asociada (ej. main, develop).")

    # Usa alias para aceptar/emitir la clave JSON 'model' sin chocar con atributos internos
    model_: NonEmptyStr = Field(
        ...,
        alias="model",
        description="Modelo asociado."
    )

    # Normalizaciones: colapsa espacios internos repetidos a uno solo
    @field_validator("name", "branch", "model_", mode="after")
    @classmethod
    def collapse_inner_spaces(cls, v: str) -> str:
        # Ya viene strippeado por str_strip_whitespace; evitamos valores vacíos tipo "   "
        if not v:
            raise ValueError("value_cannot_be_empty")
        return _SPACE_RE.sub(" ", v)