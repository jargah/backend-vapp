from fastapi import APIRouter, Depends
from interceptors.session import Session
from interceptors.credentials import Credentials

from .controller.list import operatorsList
from .controller.create import operatorsCreate
from .controller.update import operatorsUpdate
from .controller.view import operatorsView
from .controller.delete import operatorsDelete

operators = APIRouter(
    tags=['Administrator Operators'], 
    prefix='/operators', 
    dependencies=[
        Depends(Session()),
        Depends(Credentials())
    ]
)
operators.include_router(operatorsList)
operators.include_router(operatorsCreate)
operators.include_router(operatorsUpdate)
operators.include_router(operatorsView)
operators.include_router(operatorsDelete)
