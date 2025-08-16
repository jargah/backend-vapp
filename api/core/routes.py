from fastapi import APIRouter, Depends
from api.account.controller.login import login
from api.account.controller.register import register
from api.account.controller.recovery import recovery
from  interceptors.token import Token

router_core = APIRouter(
    tags=['Core'], 
    prefix='/core', 
    dependencies=[]
)
router_core.include_router(login)
router_core.include_router(register)
router_core.include_router(recovery)

