from __future__ import annotations
from typing import Optional, Annotated, Literal
from datetime import date, datetime
import re
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, StringConstraints

# Reglas básicas
_PHONE_RE = re.compile(r"^\+?[0-9][0-9\s\-]{6,20}$")

# Tipos reutilizables
NombreStr   = Annotated[str, StringConstraints(min_length=1, max_length=150)]
PhoneStr    = Annotated[str, StringConstraints(min_length=7, max_length=25)]
CPStr       = Annotated[str, StringConstraints(min_length=1, max_length=20)]
UsuarioStr  = Annotated[str, StringConstraints(min_length=3, max_length=60)]
CURPStr     = Annotated[str, StringConstraints(min_length=1, max_length=30)]
RFCStr      = Annotated[str, StringConstraints(min_length=3, max_length=20)]
PasswordStr = Annotated[str, StringConstraints(min_length=6, max_length=128, pattern=r"^[A-Za-z0-9]+$")]

class OperatorsDTO(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={"description": "DTO para lectura/validación de Operadores."},
    )

    # Identificadores y estado
    id_operador: int = Field(..., ge=1)
    id_taxi: Optional[int] = Field(None, ge=1)
    id_empresa: Optional[int] = Field(None, ge=1)
    activo: int = Field(..., ge=0, le=1)  # 0/1

    # Datos personales
    nombre: NombreStr
    ap_paterno: Optional[NombreStr] = None
    ap_materno: Optional[NombreStr] = None
    sexo: Optional[Literal["M", "F", "X"]] = None
    fecha_nacimiento: Optional[date] = None
    curp: Optional[CURPStr] = None
    rfc_operador: Optional[RFCStr] = None
    email: Optional[EmailStr] = None
    email_verificado: Optional[bool] = None
    foto: Optional[str] = ""

    # Contacto
    telefono: PhoneStr
    telefono2: Optional[PhoneStr] = None
    telefono3: Optional[PhoneStr] = None
    usuario: UsuarioStr

    # Seguridad
    password: PasswordStr  # alfanumérica, mínimo 6

    # Dirección
    calle_num: Optional[str] = None
    colonia: Optional[str] = None
    codigo_postal_operador: Optional[CPStr] = None
    estado: Optional[str] = None
    municipio: Optional[str] = None

    # Métricas y saldos
    saldo: float = 0.0
    saldo_pendiente: float = 0.0
    saldo_facturar_venapp: Optional[float] = 0.0
    calificacion: Optional[float] = Field(None, ge=0, le=5)
    viajes_realizados: Optional[int] = Field(None, ge=0)

    # Tiempos
    fecha_registro: Optional[datetime] = None
    fecha_cambio_password: Optional[datetime] = None
    hora_inicio_sesion: Optional[datetime] = None

    # Validadores
    @field_validator("email")
    @classmethod
    def _normalize_email(cls, v: Optional[EmailStr]) -> Optional[str]:
        return str(v).lower() if v is not None else None

    @field_validator("telefono", "telefono2", "telefono3")
    @classmethod
    def _validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        x = re.sub(r"\s+", " ", v.strip())
        if not _PHONE_RE.match(x):
            raise ValueError("invalid_phone_format")
        return x

    @field_validator("usuario")
    @classmethod
    def _normalize_usuario(cls, v: str) -> str:
        return v.strip()
