from fastapi import APIRouter, Depends
from  interceptors.token import Token
from interceptors.credentials import Credentials

from api.administrator.auth.routes import auth

administrator = APIRouter(
    tags=['Administrator'], 
    prefix='/administrator'
)
administrator.include_router(auth)
