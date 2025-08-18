from fastapi import APIRouter, Depends
from .controller.login import login
from interceptors.token import Token
from interceptors.credentials import Credentials

auth = APIRouter(
    tags=['Administrator Auth'], 
    prefix='/auth', 
    dependencies=[
        Depends(Token()),
        Depends(Credentials())
    ]
)
auth.include_router(login)
