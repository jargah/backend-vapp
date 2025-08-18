from fastapi import APIRouter, Depends
from interceptors.token import Token
from interceptors.credentials import Credentials

from .controller.list import operatorsList
from .controller.create import operatorsCreate
from .controller.update import operatorsUpdate
from .controller.view import operatorsView
from .controller.delete import operatorsDelete

operators = APIRouter(
    tags=['Administrator Operators Invoice'], 
    prefix='/operators-invoice', 
    dependencies=[
        Depends(Token()),
        Depends(Credentials())
    ]
)
operators.include_router(operatorsList)
operators.include_router(operatorsCreate)
operators.include_router(operatorsUpdate)
operators.include_router(operatorsView)
operators.include_router(operatorsDelete)
