from fastapi import APIRouter, Depends
from .controller.list import list
from .controller.create import create
from .controller.edit import edit
from .controller.view import view

from interceptors.session import Session
from interceptors.credentials import Credentials

typeMotor = APIRouter(
    tags=['Administrator - Tipo Motor'], 
    prefix='/type-motor', 
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
typeMotor.include_router(list)
typeMotor.include_router(create)
typeMotor.include_router(edit)
typeMotor.include_router(view)
