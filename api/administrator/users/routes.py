from fastapi import APIRouter, Depends
from .controller.list import list
from interceptors.token import Token
from interceptors.credentials import Credentials

users = APIRouter(
    tags=['Administrator - Configuration - Users'], 
    prefix='/configuration/users', 
    dependencies=[
        Depends(Token()),
        Depends(Credentials())
    ]
)
users.include_router(list)
