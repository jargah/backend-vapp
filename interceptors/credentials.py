import os
from typing import Optional, Dict, Union, List
from fastapi import Request, Depends
from sqlalchemy.orm import Session

from database.MySQL import get_db
from models.api import ApiModel
from helpers.jwt import decode as jwt_decode
from helpers.response import ExceptionResponse


class Credentials:
    """
    Valida JWT recibido en Authorization: Bearer <token>.
    - Verifica firma y expiración (helpers.jwt.decode exige 'exp').
    - Opcionalmente verifica 'aud' y 'iss' si se activan flags.
    - Guarda en request.state.session = {'token': str, 'jwt': dict, 'api': dict}
    """

    def __init__(
        self,
        *,
        require_audience: bool = False,
        require_issuer: bool = False,
        leeway: int = 5,
    ):
        self.require_audience = require_audience
        self.require_issuer = require_issuer
        self.leeway = leeway

    @staticmethod
    def _get_bearer_token(request: Request) -> Optional[str]:
        auth = request.headers.get("Authorization")
        if not auth:
            return None
        parts = auth.split()
        if len(parts) != 2:
            return None
        scheme, token = parts
        if scheme.lower() != "bearer":
            return None
        return token

    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        # 1) Leer Bearer
        token = self._get_bearer_token(request)
        if not token:
            raise ExceptionResponse(status_code=401, details=["error_token_required"])
        

        jwt_result = jwt_decode(
            token
        )
        
        print(jwt_result)

        if not jwt_result.get("success"):
            # Normaliza códigos según helpers.jwt.decode (los nombres deben coincidir)
            code = jwt_result.get("error") or "error_token_invalid"

            # Mapea a HTTP status
            status_map_401 = {
                "error_token_expired",
                "error_token_immature",        # nbf en futuro
                "error_token_audience",        # aud inválido
                "error_token_issuer",          # iss inválido
                "error_token_signature",       # firma inválida
                "error_token_iat",             # iat inválido
                "error_token_missing_claim",   # falta 'exp' u otro require
                "error_token_malformed",       # formato JWT incorrecto
                "error_token_invalid",         # catch-all inválido
            }
            if code == "error_token_key_empty":
                status = 500
            elif code in status_map_401:
                status = 401
            else:
                status = 400  # por defecto, mal request

            raise ExceptionResponse(status_code=status, details=[code])

        payload: Dict = jwt_result["data"]
        
        print(payload)

        # 3) Colgar en request.state.session
        if not hasattr(request.state, "session") or request.state.session is None:
            request.state.session = {}
        request.state.session["token"] = token
        request.state.session["jwt"] = payload

        # 4) Validación contra tu tabla de APIs (según claim dentro del payload)
        #    OJO: aquí asumo que el JWT incluye un claim 'token' de tu API.
        api_token_claim = payload.get("token")
        if not api_token_claim:
            # si prefieres usar otro claim, cámbialo aquí
            raise ExceptionResponse(status_code=401, details=["error_token_invalid"])

        mApi = ApiModel(db)
        api = await mApi.selectFirst("token = '{token}'".format(token=api_token_claim))
        if api is None:
            raise ExceptionResponse(status_code=401, details=["error_token_invalid"])

        # 5) Validar environment vs STAGE
        stage = os.getenv("STAGE")
        if stage and api.get("environment") != stage:
            raise ExceptionResponse(status_code=401, details=["error_token_environment"])

        request.state.session["api"] = api

        # Dependency no necesita devolver nada; el hecho de no lanzar excepción ya “autoriza”
        return
