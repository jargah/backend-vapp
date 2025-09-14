from fastapi import APIRouter, Depends
from .controller.login import login
from interceptors.credentials import Credentials

auth = APIRouter(
    tags=['Administrator Auth'], 
    prefix='/auth', 
    dependencies=[
        Depends(Credentials())
    ]
)
auth.include_router(login)
