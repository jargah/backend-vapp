from fastapi import APIRouter, Depends
from api.account.controller.login import login
from api.account.controller.register import register
from api.account.controller.recovery import recovery
from  interceptors.token import Token
from interceptors.credentials import Credentials

router_account = APIRouter(
    tags=['Account'], 
    prefix='/account', 
    dependencies=[
        Depends(Token()),
        Depends(Credentials())
    ]
)
router_account.include_router(login)
router_account.include_router(register)
router_account.include_router(recovery)
