from fastapi import APIRouter, Depends
from interceptors.token import Token
from interceptors.credentials import Credentials

from .controller.list import referralList
from .controller.create import referralCreate
from .controller.update import referralUpdate
from .controller.view import referralView
from .controller.delete import referralDelete

referral = APIRouter(
    tags=['Administrator Referral'], 
    prefix='/referral', 
    dependencies=[
        Depends(Token()),
        Depends(Credentials())
    ]
)
referral.include_router(referralList)
referral.include_router(referralCreate)
referral.include_router(referralUpdate)
referral.include_router(referralView)
referral.include_router(referralDelete)
