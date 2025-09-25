import jwt
from jwt import (
    PyJWTError,
    InvalidTokenError,
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAudienceError,
    InvalidIssuedAtError,
    InvalidIssuerError,
    InvalidKeyError,
    InvalidAlgorithmError,
    MissingRequiredClaimError,
    InvalidSignatureError,
)
from typing import Any, Dict, Optional, Union, Iterable, TypedDict, Mapping
import os
from datetime import datetime, timedelta, timezone

def _utcnow():
    return datetime.now(timezone.utc)

def _format_error(e: Exception) -> Dict[str, str]:
    def pack(code: str, message: str) -> Dict[str, str]:
        return {"code": code, "message": message}

    if isinstance(e, ExpiredSignatureError):
        return pack("ExpiredSignatureError", "error_token_expired")
    if isinstance(e, ImmatureSignatureError):
        return pack("ImmatureSignatureError", "error_token_immature")
    if isinstance(e, InvalidAudienceError):
        return pack("InvalidAudienceError", "error_token_audience_invalid")
    if isinstance(e, InvalidIssuerError):
        return pack("InvalidIssuerError", "error_token_issuer_invalid")
    if isinstance(e, InvalidIssuedAtError):
        return pack("InvalidIssuedAtError", "error_token_iat_invalid")
    if isinstance(e, MissingRequiredClaimError):
        # si PyJWT provee e.claim, puedes agregarla aparte si la quieres loguear
        return pack("MissingRequiredClaimError", "error_token_claim_missing")
    if isinstance(e, InvalidSignatureError):
        return pack("InvalidSignatureError", "error_token_signature_invalid")
    if isinstance(e, InvalidAlgorithmError):
        return pack("InvalidAlgorithmError", "error_token_algorithm_invalid")
    if isinstance(e, InvalidKeyError):
        return pack("InvalidKeyError", "error_token_key_invalid")
    if isinstance(e, DecodeError):
        return pack("DecodeError", "error_token_decode_error")
    if isinstance(e, InvalidTokenError):
        return pack("InvalidTokenError", "error_token_invalid")
    if isinstance(e, PyJWTError):
        return pack("PyJWTError", "error_token_pyjwt")
    return pack(type(e).__name__, "error_token_unknown")

def create(
    payload: Dict[str, Any],
    algorithm: str = "HS256",
    expires_minutes: Optional[Union[int, float]] = None,
    expires_in: Optional[Union[int, float, timedelta]] = None,
):
    try:
        claims = payload.copy()
        now = _utcnow()
        ts = int(now.timestamp())
        
        claims["iat"] = ts
        claims["nbf"] = ts
        
        exp_dt: Optional[datetime] = None
        if expires_minutes is not None:
            exp_dt = now + timedelta(minutes=float(expires_minutes))
        elif expires_in is not None:
            if isinstance(expires_in, (int, float)):
                exp_dt = now + timedelta(seconds=float(expires_in))
            elif isinstance(expires_in, timedelta):
                exp_dt = now + expires_in
            else:
                raise TypeError("expires_in debe ser int, float, timedelta o None")
        if exp_dt is not None:
            claims["exp"] = int(exp_dt.timestamp())

        token = jwt.encode(claims, os.getenv('JWT_SECRET'), algorithm=algorithm)
        return token
    except Exception as e:
        return None

def verify(
    token: str,
    algorithms: Iterable[str] = ("HS256"),
    key: str = None
):
    
    print(key if key != None else os.getenv('JWT_SECRET'))

    try:
        
        options = {"verify_exp": True}
        
        payload = jwt.decode(
            token,
            key if key != None else os.getenv('JWT_SECRET'),
            algorithms=list(algorithms),
            options=options,
        )
    
        
        return {
            "success": True, 
            "payload": payload
        }
        
    except (
        ExpiredSignatureError,
        ImmatureSignatureError,
        InvalidAudienceError,
        InvalidIssuerError,
        InvalidIssuedAtError,
        MissingRequiredClaimError,
        InvalidSignatureError,
        InvalidAlgorithmError,
        InvalidKeyError,
        DecodeError,
        InvalidTokenError,
        PyJWTError,
    ) as e:
        return {
            "success": False, 
            "error": _format_error(e)
        }