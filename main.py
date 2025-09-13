import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_400_BAD_REQUEST
from dotenv import load_dotenv
from middlewares.error_handler import ErrorHandler
from middlewares.database import Database
from api.routes import router
from helpers.routing import setRoutes
from helpers.response import ExceptionResponse, ResponseHelper
from pydantic import BaseModel, EmailStr, Field
from typing import Any, Dict, List, Optional

load_dotenv()

app = FastAPI()
app.title = os.getenv('APP_NAME')
app.version = '1.0.0'
app.add_middleware(ErrorHandler)
app.add_middleware(Database)

setRoutes(app, router)

@app.exception_handler(ExceptionResponse)
async def custom_error_handler(request: Request, exc: ExceptionResponse):
    
    return ResponseHelper(
        code=exc.status_code,
        errors=exc.details
    )
    
# ------------------------------------------
# Tabla de mensajes por tipo (Pydantic v2 + alias v1)
# ------------------------------------------
TYPE_MESSAGES: Dict[str, str] = {
    # Faltantes / nulos
    "missing": "El campo '{field}' es obligatorio.",
    "value_error.missing": "El campo '{field}' es obligatorio.",
    "none_required": "El campo '{field}' no puede ser nulo.",
    "none_type": "El campo '{field}' no puede ser nulo.",

    # Tipos / parsing
    "string_type": "El campo '{field}' debe ser una cadena.",
    "bytes_type": "El campo '{field}' debe ser bytes.",
    "int_parsing": "El campo '{field}' debe ser un número entero.",
    "int_type": "El campo '{field}' debe ser un número entero.",
    "float_parsing": "El campo '{field}' debe ser un número.",
    "float_type": "El campo '{field}' debe ser un número.",
    "bool_parsing": "El campo '{field}' debe ser verdadero o falso.",
    "bool_type": "El campo '{field}' debe ser verdadero o falso.",
    "list_type": "El campo '{field}' debe ser una lista.",
    "tuple_type": "El campo '{field}' debe ser una tupla.",
    "set_type": "El campo '{field}' debe ser un conjunto.",
    "dict_type": "El campo '{field}' debe ser un objeto/dict.",
    "mapping_type": "El campo '{field}' debe ser un objeto/dict.",
    # Aliases v1
    "type_error.integer": "El campo '{field}' debe ser un número entero.",
    "type_error.float": "El campo '{field}' debe ser un número.",
    "type_error.bool": "El campo '{field}' debe ser verdadero o falso.",
    "type_error.list": "El campo '{field}' debe ser una lista.",
    "type_error.dict": "El campo '{field}' debe ser un objeto/dict.",

    # Strings / bytes
    "string_too_short": "El campo '{field}' debe tener al menos {min_length} caracteres.",
    "string_too_long": "El campo '{field}' debe tener como máximo {max_length} caracteres.",
    "string_pattern_mismatch": "Formato inválido en '{field}'.",
    "pattern_mismatch": "Formato inválido en '{field}'.",
    "bytes_too_short": "El campo '{field}' (bytes) debe tener al menos {min_length} bytes.",
    "bytes_too_long": "El campo '{field}' (bytes) debe tener como máximo {max_length} bytes.",
    # Aliases v1
    "value_error.any_str.min_length": "El campo '{field}' debe tener al menos {limit_value} caracteres.",
    "value_error.any_str.max_length": "El campo '{field}' debe tener como máximo {limit_value} caracteres.",
    "value_error.regex": "Formato inválido en '{field}'.",

    # Números / rangos
    "greater_than": "El campo '{field}' debe ser mayor que {gt}.",
    "greater_than_equal": "El campo '{field}' debe ser mayor o igual que {ge}.",
    "less_than": "El campo '{field}' debe ser menor que {lt}.",
    "less_than_equal": "El campo '{field}' debe ser menor o igual que {le}.",
    "multiple_of": "El campo '{field}' debe ser múltiplo de {multiple_of}.",
    "finite_number": "El campo '{field}' debe ser un número finito.",
    # Aliases v1
    "value_error.number.not_ge": "El campo '{field}' debe ser mayor o igual que {limit_value}.",
    "value_error.number.not_gt": "El campo '{field}' debe ser mayor que {limit_value}.",
    "value_error.number.not_le": "El campo '{field}' debe ser menor o igual que {limit_value}.",
    "value_error.number.not_lt": "El campo '{field}' debe ser menor que {limit_value}.",
    "value_error.number.not_multiple": "El campo '{field}' debe ser múltiplo de {multiple_of}.",
    "value_error.number.not_finite": "El campo '{field}' debe ser un número finito.",

    # Listas / tuplas / sets
    "list_too_short": "El campo '{field}' debe tener al menos {min_length} elementos.",
    "list_too_long": "El campo '{field}' debe tener como máximo {max_length} elementos.",
    "tuple_too_short": "La tupla '{field}' debe tener al menos {min_length} elementos.",
    "tuple_too_long": "La tupla '{field}' debe tener como máximo {max_length} elementos.",
    "tuple_length_mismatch": "La tupla '{field}' debe tener exactamente {expected_length} elementos.",
    "set_too_short": "El conjunto '{field}' debe tener al menos {min_length} elementos.",
    "set_too_long": "El conjunto '{field}' debe tener como máximo {max_length} elementos.",
    "too_short": "El campo '{field}' tiene muy pocos elementos (mínimo {min_length}).",
    "too_long": "El campo '{field}' tiene demasiados elementos (máximo {max_length}).",

    # Fecha / hora
    "date_parsing": "El campo '{field}' debe ser una fecha válida (YYYY-MM-DD).",
    "time_parsing": "El campo '{field}' debe ser una hora válida (HH:MM[:SS]).",
    "datetime_parsing": "El campo '{field}' debe ser una fecha/hora válida.",
    "naive_datetime_not_allowed": "El campo '{field}' debe incluir zona horaria.",
    "aware_datetime_required": "El campo '{field}' debe incluir zona horaria.",

    # Formatos especiales
    "value_error.email": "El campo '{field}' debe ser un correo electrónico válido.",
    "value_error.url": "El campo '{field}' debe ser una URL válida.",
    "value_error.uuid": "El campo '{field}' debe ser un UUID válido.",
    "value_error.decimal": "El campo '{field}' debe ser un decimal válido.",
    "value_error.json": "El campo '{field}' debe ser un JSON válido.",
    "value_error.hostname": "El campo '{field}' debe ser un hostname válido.",
    "value_error.ipv4": "El campo '{field}' debe ser una IPv4 válida.",
    "value_error.ipv6": "El campo '{field}' debe ser una IPv6 válida.",
    "value_error.ipvany": "El campo '{field}' debe ser una IP válida.",

    # Enum / Literal / Union
    "enum": "El campo '{field}' debe ser uno de: {expected}.",
    "literal_error": "El campo '{field}' debe ser uno de: {expected}.",
    "union": "El valor de '{field}' no coincide con ninguno de los tipos permitidos.",
    "no_such_attribute": "El campo '{field}' no es válido.",

    # Fallbacks
    "value_error": "Dato inválido en '{field}'.",
    "type_error": "Tipo inválido en '{field}'.",
}

# ------------------------------------------
# Overrides por campo (opcional)
# ------------------------------------------
FIELD_OVERRIDES: Dict[str, Dict[str, str]] = {
    # "password": {
    #     "string_too_short": "La contraseña debe tener al menos {min_length} caracteres.",
    #     "pattern_mismatch": "La contraseña no cumple el formato requerido.",
    # },
    # "username": { "value_error.email": "Debes ingresar un correo válido." },
}


# ------------------------------------------
# Helpers de formateo
# ------------------------------------------
def _join_loc(loc: List[Any]) -> str:
    """
    ('body','items',2,'name') -> items[2].name
    """
    skip = {"body", "query", "path", "header"}
    parts: List[str] = []
    for p in loc:
        if p in skip:
            continue
        if isinstance(p, int):
            if parts:
                parts[-1] = f"{parts[-1]}[{p}]"
            else:
                parts.append(f"[{p}]")
        else:
            parts.append(str(p))
    return ".".join(parts) if parts else "body"


def _pick_template(etype: str) -> Optional[str]:
    """
    Busca plantilla por:
    1) tipo exacto
    2) sin último segmento tras '.'
    3) sin sufijo tras ':'
    4) primer segmento antes del '.'
    """
    return (
        TYPE_MESSAGES.get(etype)
        or TYPE_MESSAGES.get(etype.rsplit(".", 1)[0])
        or TYPE_MESSAGES.get(etype.split(":", 1)[0])
        or TYPE_MESSAGES.get(etype.split(".", 1)[0])
    )


def _format_message(field: str, etype: str, msg: str, ctx: Optional[Dict[str, Any]]) -> str:
    # Override por campo
    if field in FIELD_OVERRIDES and etype in FIELD_OVERRIDES[field]:
        template = FIELD_OVERRIDES[field][etype]
    else:
        template = _pick_template(etype)

    if template is None:
        # Fallback al msg original de Pydantic
        return msg

    values: Dict[str, Any] = {"field": field}
    if ctx:
        values.update(ctx)
        # Normalizaciones v1/v2
        if "limit_value" in ctx and "min_length" not in ctx and "max_length" not in ctx:
            values.setdefault("min_length", ctx["limit_value"])
            values.setdefault("max_length", ctx["limit_value"])
        if "permitted" in ctx and "expected" not in ctx:
            values["expected"] = ", ".join(map(str, ctx["permitted"]))

    try:
        return template.format(**values)
    except Exception:
        try:
            return template.format(field=field)
        except Exception:
            return msg


def format_validation_errors(exc: RequestValidationError) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for err in exc.errors():
        loc = err.get("loc", [])
        field = _join_loc(loc)
        etype = err.get("type", "") or ""
        base_msg = err.get("msg", "Dato inválido")
        ctx = err.get("ctx", {}) or {}
        final_msg = _format_message(field, etype, base_msg, ctx)
        out.setdefault(field, []).append(final_msg)
    return out


# ------------------------------------------
# Handler global 422
# ------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = format_validation_errors(exc)
    return ResponseHelper(
        code=HTTP_400_BAD_REQUEST,
        message="Validación fallida",
        data=errors,
    )


@app.get('/', tags=['home'])
def root():
    return HTMLResponse('<h1>VENAPP</h1>')

