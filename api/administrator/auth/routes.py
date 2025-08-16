from fastapi import APIRouter, Depends
from api.account.controller.login import login
from api.account.controller.register import register
from api.account.controller.recovery import recovery
from interceptors.token import Token
from interceptors.credentials import Credentials

auth = APIRouter(
    prefix='/auth', 
    dependencies=[
        Depends(Token()),
        Depends(Credentials())
    ]
)
auth.include_router(login)
auth.include_router(register)
auth.include_router(recovery)
