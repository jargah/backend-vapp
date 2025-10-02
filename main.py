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
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
app.title = os.getenv('APP_NAME')
app.version = '1.0.0'


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandler)
app.add_middleware(Database)

setRoutes(app, router)

@app.exception_handler(ExceptionResponse)
async def custom_error_handler(request: Request, exc: ExceptionResponse):
    
    return ResponseHelper(
        code=exc.status_code,
        errors=exc.details,
        message='Request failed'
    )


# ------------------------------------------
# Handler global 422
# ------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ResponseHelper(
        code=HTTP_400_BAD_REQUEST,
        message="Validación fallida",
        data=exc,
    )


@app.get('/', tags=['home'])
def root():
    return HTMLResponse('<h1>VENAPP</h1>')


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}