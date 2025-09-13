from fastapi import HTTPException, Request, Header
from fastapi.security import HTTPBearer, APIKeyHeader
from helpers.jwt import create, decode
from starlette.middleware.base import BaseHTTPMiddleware
from utils.globals import parseDict

class Token(HTTPBearer):
    async def __call__(self, request: Request):
        
        auth = await super().__call__(request)
        data = decode(auth.credentials)

        if data == None:
            print('errr')
            raise HTTPException(
                status_code=401,
                detail='error_token_bearer_invalid'
            )
        
        request.state.session = data