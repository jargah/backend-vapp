# helpers/jwt.py
from typing import Optional, Dict, Any, Union,  List
import os
from datetime import datetime, timedelta, timezone
import jwt
from jwt import (
    ExpiredSignatureError,
    InvalidSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidIssuedAtError,
    InvalidKeyError,
    InvalidAudienceError,
    InvalidIssuerError,
    MissingRequiredClaimError,
    DecodeError,
    InvalidTokenError,
)

# =========================
# Helpers de tiempo / exp
# =========================

def _iso_to_datetime_utc(value: str) -> datetime:
    v = value.strip()
    if v.endswith('Z'):
        v = v[:-1]
        dt = datetime.fromisoformat(v)
        return dt.replace(tzinfo=timezone.utc)
    dt = datetime.fromisoformat(v)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def _to_epoch(dt_or_epoch: Union[int, float, datetime, str]) -> int:
    if isinstance(dt_or_epoch, (int, float)):
        return int(dt_or_epoch)
    if isinstance(dt_or_epoch, str):
        return int(_iso_to_datetime_utc(dt_or_epoch).timestamp())
    if isinstance(dt_or_epoch, datetime):
        if dt_or_epoch.tzinfo is None:
            dt_or_epoch = dt_or_epoch.replace(tzinfo=timezone.utc)
        else:
            dt_or_epoch = dt_or_epoch.astimezone(timezone.utc)
        return int(dt_or_epoch.timestamp())
    raise ValueError("unsupported_exp_type")

def _to_int(v) -> Optional[int]:
    if v is None:
        return None
    try:
        return int(v)
    except Exception:
        return None

def _exp_dt(
    *,
    now: datetime,
    exp_at: Optional[Union[int, float, datetime, str]] = None,
    exp_seconds: Optional[int] = None,
    exp_minutes: Optional[int] = None,
    fallback_payload_exp: Optional[Union[int, float, datetime, str]] = None,
    default_hours: int = 24,
) -> datetime:
    # 1) Absoluto
    if isinstance(exp_at, datetime):
        dt = exp_at
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    if isinstance(exp_at, (int, float)):
        return datetime.fromtimestamp(int(exp_at), tz=timezone.utc)
    if isinstance(exp_at, str):
        return _iso_to_datetime_utc(exp_at)

    # 2) Relativo
    if exp_seconds is not None:
        return now + timedelta(seconds=exp_seconds)
    if exp_minutes is not None:
        return now + timedelta(minutes=exp_minutes)

    # 3) Si el payload ya traía exp
    if fallback_payload_exp is not None:
        # Permitimos int/float/dt/ISO
        if isinstance(fallback_payload_exp, (int, float)):
            return datetime.fromtimestamp(int(fallback_payload_exp), tz=timezone.utc)
        if isinstance(fallback_payload_exp, str):
            return _iso_to_datetime_utc(fallback_payload_exp)
        if isinstance(fallback_payload_exp, datetime):
            dt = fallback_payload_exp
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)

    # 4) Por defecto 24h
    return now + timedelta(hours=default_hours)

# =========================
# Create (firmado)
# =========================

def create(
    payload: Dict,
    *,
    exp_at: Optional[Union[int, float, datetime, str]] = None,  # fecha/hora absoluta
    exp_seconds: Optional[Union[int, str]] = None,              # TTL seg
    exp_minutes: Optional[Union[int, str]] = None,              # TTL min
    add_iat: bool = True,
    add_nbf_now: bool = False,
    debug: bool = False,
) -> Dict[str, Any]:
    try:
        key = os.getenv("JWT_TOKEN")
        if not key:
            return {'success': False, 'error': 'error_token_key_empty'}

        now = datetime.now(timezone.utc)
        claims = dict(payload or {})

        # Coerción segura
        exp_seconds_i = _to_int(exp_seconds)
        exp_minutes_i = _to_int(exp_minutes)

        exp_dt = _exp_dt(
            now=now,
            exp_at=exp_at,
            exp_seconds=exp_seconds_i,
            exp_minutes=exp_minutes_i,
            fallback_payload_exp=claims.get("exp"),
            default_hours=24,
        )

        if exp_dt <= now:
            return {'success': False, 'error': 'error_exp_in_past'}

        # PyJWT acepta datetime aware en 'exp'
        claims["exp"] = exp_dt

        if add_iat and "iat" not in claims:
            claims["iat"] = int(now.timestamp())

        if add_nbf_now and "nbf" not in claims:
            claims["nbf"] = int(now.timestamp())

        token: str = jwt.encode(payload=claims, key=key, algorithm="HS256")

        return {
            'success': True,
            'data': {
                'token': token,
                'exp': int(exp_dt.timestamp())
            }
        }

    except InvalidAlgorithmError:
        resp = {'success': False, 'error': 'error_sign_invalid_algorithm'}
    except InvalidKeyError:
        resp = {'success': False, 'error': 'error_sign_invalid_key'}
    except ValueError as err:
        resp = {'success': False, 'error': 'error_exp_invalid'}
        if debug:
            resp['detail'] = str(err)
    except Exception as err:
        resp = {'success': False, 'error': 'error_sign_unknown'}
        if debug:
            resp['detail'] = str(err)
    return resp

# =========================
# Decode (verificado)
# =========================

def _dt_to_epoch(v):
    if isinstance(v, datetime):
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        else:
            v = v.astimezone(timezone.utc)
        return int(v.timestamp())
    return v


def decode(
    token: str,
    *,
    audience: Optional[Union[str, List[str]]] = None,
    issuer: Optional[str] = None,
    leeway: int = 0,
    debug: bool = False,

    # NUEVO: flexibiliza requisitos
    require_exp: bool = False,
    require_iat: bool = False,
    require_nbf: bool = False,

    # NUEVO: controla verificaciones (por defecto, exp se verifica solo si viene)
    verify_exp: Optional[bool] = None,  # None => True pero SIN exigir que exista 'exp'
) -> Dict[str, Any]:
    """
    Verifica firma siempre. Por defecto:
      - NO exige 'exp' (ni otros) si no vienen.
      - SÍ valida 'exp' si existe en el token (y respeta 'leeway').
      - 'aud'/'iss' solo se validan si los pasas.
    Puedes volverlo estricto con require_exp/iat/nbf=True.
    """
    try:
        key = os.getenv("JWT_TOKEN")
        if not key:
            return {'success': False, 'error': 'error_token_key_empty'}

        # Si no especificas, verificamos expiración si existe 'exp' (comportamiento sano)
        if verify_exp is None:
            verify_exp = True

        # Construye la lista de claims requeridos según flags
        required_claims = []
        if require_exp:
            required_claims.append("exp")
        if require_iat:
            required_claims.append("iat")
        if require_nbf:
            required_claims.append("nbf")

        data = jwt.decode(
            token,
            key,
            algorithms=["HS256"],
            audience=audience,
            issuer=issuer,
            options={
                "verify_signature": True,
                "verify_exp": bool(verify_exp),   # valida exp si está; solo la exige si está en "require"
                "require": required_claims,       # exige solo lo que pidas
                # 'verify_nbf' y 'verify_iat' están activos por defecto si existen los claims
            },
            leeway=leeway,
        )

        # Normaliza tiempos a epoch int si vinieron como datetime (puede suceder)
        for k in ("exp", "iat", "nbf"):
            if k in data:
                data[k] = _dt_to_epoch(data[k])

        return {'success': True, 'data': data}

    except ExpiredSignatureError:
        return {'success': False, 'error': 'error_token_expired'}
    except ImmatureSignatureError:
        return {'success': False, 'error': 'error_token_immature'}   # nbf en futuro
    except InvalidAudienceError:
        return {'success': False, 'error': 'error_token_audience'}
    except InvalidIssuerError:
        return {'success': False, 'error': 'error_token_issuer'}
    except MissingRequiredClaimError as e:
        return {'success': False, 'error': 'error_token_missing_claim', 'detail': str(e) if debug else None}
    except InvalidSignatureError:
        return {'success': False, 'error': 'error_token_signature'}
    except InvalidIssuedAtError:
        return {'success': False, 'error': 'error_token_iat'}
    except DecodeError:
        return {'success': False, 'error': 'error_token_malformed'}
    except InvalidTokenError:
        return {'success': False, 'error': 'error_token_invalid'}
    except Exception as e:
        return {'success': False, 'error': 'error_decode_unknown', 'detail': str(e) if debug else None}