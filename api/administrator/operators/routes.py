from fastapi import APIRouter, Depends
from .controller.list import list
from .controller.create import create
from .controller.edit import edit
from .controller.view import view
from .controller.delete import deleted

from interceptors.session import Session
from interceptors.credentials import Credentials

operators = APIRouter(
    tags=['Administrator - Operators'], 
    prefix='/operators', 
    dependencies=[
        #Depends(Session()),
        Depends(Credentials(
            require_audience=True,
            require_issuer=True, 
            leeway=10
        )),
        Depends(Session())
    ]
)
operators.include_router(list)
operators.include_router(create)
operators.include_router(edit)
operators.include_router(view)
operators.include_router(deleted)
