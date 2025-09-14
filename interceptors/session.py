from typing import Optional, Dict, Any, Union, List
import os
from fastapi import Request
from helpers.response import ExceptionResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from helpers.jwt import decode as jwt_decode
from utils.globals import parseDict

def _looks_like_jwt(token: str) -> bool:
    return token.count(".") == 2

def _normalize_decode_result(res: Any) -> Dict[str, Any]:
    if res is None:
        return {'ok': False, 'payload': None, 'error': 'error_token_bearer_invalid'}
    if isinstance(res, dict) and 'success' in res:
        if res.get('success') and isinstance(res.get('data'), dict):
            return {'ok': True, 'payload': res['data'], 'error': None}
        return {'ok': False, 'payload': None, 'error': res.get('error') or 'error_token_bearer_invalid'}
    if isinstance(res, dict):
        return {'ok': True, 'payload': res, 'error': None}
    return {'ok': False, 'payload': None, 'error': 'error_token_bearer_invalid'}

class Session(HTTPBearer):
    def __init__(self, *, require_audience: bool = False, require_issuer: bool = False, leeway: int = 5, auto_error: bool = False) -> None:
        super().__init__(auto_error=auto_error)
        self.require_audience = require_audience
        self.require_issuer = require_issuer
        self.leeway = leeway

    async def __call__(self, request: Request) -> Dict[str, Any]:
        # 1) Solo header 'sesion'
        token: Optional[str] = request.headers.get('session')

        if not token:
            raise ExceptionResponse(
                status_code=401, 
                details=[
                    "error_session_required"
                ]
            )

        # 2) base de session
        if not hasattr(request.state, "session") or not isinstance(getattr(request.state, "session"), dict):
            request.state.session = {}

        session_dict: Dict[str, Any] = dict(request.state.session)
        session_dict["token"] = token
        session_dict["token_type"] = "session"
        session_dict["jwt"] = None

        # 3) Intentar decodificar si *parece* JWT
        if _looks_like_jwt(token):
            audience = os.getenv("JWT_AUD") if self.require_audience else None
            issuer = os.getenv("JWT_ISS") if self.require_issuer else None

            res = jwt_decode(token, require_exp=True, leeway=5)
            norm = _normalize_decode_result(res)

            if norm["ok"] and isinstance(norm["payload"], dict):
                session_dict["jwt"] = norm["payload"]
                session_dict["token_type"] = "jwt"

        try:
            session_dict = parseDict(session_dict)
        except Exception:
            pass

        request.state.session = session_dict
        return session_dict
