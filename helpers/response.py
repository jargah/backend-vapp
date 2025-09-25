from typing import Any, Optional
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
import decimal

class ResponseHelper(JSONResponse):
    def __init__(self, code: int = status.HTTP_200_OK, message: Optional[str] = None,  errors: Optional[Any] = None, data: Any = None):
        self.code = code
        self.message = message or []
        self.data = data or None
        self.errors = errors or []
        
        super().__init__(status_code=self.code, content=self.to_dict())
    
    def to_dict(self):
        
        data = jsonable_encoder(self.data)
        return {
            'status': self.code,
            'message': self.message,
            'errors': self.errors,
            'data': data
        }

class ExceptionResponse(HTTPException):
    def __init__(self, error: str = None, status_code: int = status.HTTP_400_BAD_REQUEST, details: dict = None):
        super().__init__(status_code=status_code, detail=details)
        self.details = details or error or {} 

    def to_dict(self):
        return {
            'status': self.status_code,
            'error': self.detail,
        }
        
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return (str(o) for o in [o])
        return super(DecimalEncoder, self).default(o)