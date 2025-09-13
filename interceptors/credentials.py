from fastapi import HTTPException, Request, Header, Depends
from fastapi.security import HTTPBearer, APIKeyHeader
from helpers.jwt import create, decode
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from database.MySQL import get_db, rawDB
from models.api import ApiModel
from helpers.response import ExceptionResponse
import os

class Credentials:
    
    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        
        session_data = getattr(request.state, "session", None) or {}
        token = session_data.get("token")
        
        if not token:
            raise ExceptionResponse(
                details=['error_token_required']
            )  
        
        mApi = ApiModel(db)
        api = await mApi.selectFirst("token = '{token}'".format(token=token))
        
        if api == None:
            
            raise ExceptionResponse(
                details=['error_token_invalid']
            )    
        
        if api['environment'] != os.getenv('STAGE'):
            raise ExceptionResponse(
                details=['error_token_environment']
            )  
        
        pass

