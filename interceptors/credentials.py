from fastapi import HTTPException, Request, Header
from fastapi.security import HTTPBearer, APIKeyHeader
from helpers.jwt import create, decode
from starlette.middleware.base import BaseHTTPMiddleware

class Credentials:
    async def __call__(self, request: Request):
        pass

