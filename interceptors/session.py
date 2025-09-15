from typing import Optional, Dict, Any, Union, List
import os
from fastapi import Request
from helpers.response import ExceptionResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from helpers.jwt import verify
from utils.globals import parseDict

def _looks_like_jwt(token: str) -> bool:
    return token.count(".") == 2

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

            res = verify(token)
            
            if res.get('success') == False:
                raise ExceptionResponse(
                    status_code=401, 
                    details=[
                        res['error']['message']
                    ]
                )
                
            if res.get('success') and isinstance(res.get('payload'), dict):
                print(1)
                session_dict["jwt"] = res.get('payload')
                session_dict["token_type"] = "jwt"
                

        try:
            session_dict = parseDict(session_dict)
        except Exception:
            pass

        request.state.session = session_dict
        return session_dict
