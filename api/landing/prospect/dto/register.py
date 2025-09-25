from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
import re

PHONE_RE = re.compile(r"^\d{7,20}$")          # Solo dígitos, 7-20
YEAR_RE  = re.compile(r"^\d{4}$")             # YYYY
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")  # Regex básica de email


class VehicleDTO(BaseModel):
    branch: int = Field(..., description="ID de marca/sucursal del vehículo")
    model: str = Field(..., min_length=1, max_length=50, description="Modelo comercial")
    year: str = Field(..., description="Año en formato YYYY")
    number_plate: Optional[str] = Field(
        None, min_length=0, max_length=20, description="Placa del vehículo (solo operador)"
    )

    @field_validator("model", mode="before")
    @classmethod
    def _strip_model(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("year", mode="before")
    @classmethod
    def _strip_year(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("year")
    @classmethod
    def _validate_year(cls, v):
        if not YEAR_RE.match(v):
            raise ValueError("El campo 'year' debe tener el formato YYYY (4 dígitos).")
        return v

    @field_validator("number_plate", mode="before")
    @classmethod
    def _strip_plate(cls, v):
        return v.strip() if isinstance(v, str) else v


class RegisterDTO(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=80)
    last_name: str = Field(..., min_length=1, max_length=80)
    second_surname: Optional[str] = Field(None, min_length=1, max_length=80)
    email: Optional[str] = Field(None, description="Correo electrónico del usuario")
    phone: Optional[str] = Field(
        None,
        description="Solo dígitos. Ajusta el patrón en PHONE_RE si requieres formato distinto.",
    )
    is_fleet: bool = False
    is_operator: bool = False
    vehicles: List[VehicleDTO] = Field(default_factory=list)

    # --- Normalizaciones básicas ---
    @field_validator("first_name", "last_name", "second_surname", mode="before")
    @classmethod
    def _strip_names(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("email")
    @classmethod
    def _validate_email(cls, v):
        if v is None or v == "":
            return v
        v = v.strip()
        if not EMAIL_RE.match(v):
            raise ValueError("El correo electrónico no es válido.")
        return v

    @field_validator("phone")
    @classmethod
    def _validate_phone(cls, v):
        if v is None or v == "":
            return v
        v = v.strip()
        if not PHONE_RE.match(v):
            raise ValueError("El teléfono debe contener solo dígitos (7 a 20).")
        return v

    # --- Reglas condicionales para vehicles ---
    @model_validator(mode="after")
    def _validate_vehicle_rules(self):
        # Si cualquiera de los flags es True, debe haber al menos 1 vehículo
        if (self.is_operator or self.is_fleet) and len(self.vehicles) == 0:
            raise ValueError("El arreglo 'vehicles' no puede estar vacío cuando 'is_operator' o 'is_fleet' es verdadero.")

        # Regla: operador → number_plate obligatorio
        if self.is_operator:
            print(22)
            for idx, v in enumerate(self.vehicles):
                if not v.number_plate:
                    raise ValueError(f"'vehicles[{idx}].number_plate' es obligatorio para operadores.")

        # Regla: flota → number_plate NO permitido con valor
        """ if self.is_fleet:
            for idx, v in enumerate(self.vehicles):
                if v.number_plate not in (None, "",):
                    raise ValueError(f"'vehicles[{idx}].number_plate' no está permitido para flotas.") """
        return self

