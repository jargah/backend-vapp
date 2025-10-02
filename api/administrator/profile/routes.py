from fastapi import APIRouter, Depends
from .controller.me import me
from interceptors.credentials import Credentials
from interceptors.session import Session

profile = APIRouter(
    tags=['Administrator Profile'], 
    prefix='/profile', 
    dependencies=[
        Depends(Credentials()),
        Depends(Session())
    ]
)
profile.include_router(me)
