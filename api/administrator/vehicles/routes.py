from fastapi import APIRouter, Depends
from .controller.list import list
from .controller.create import create
from .controller.edit import edit
from .controller.view import view
from .controller.delete import deleted

from interceptors.session import Session
from interceptors.credentials import Credentials

vehicles = APIRouter(
    tags=['Administrator - Vehicles'], 
    prefix='/vehicles', 
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
vehicles.include_router(list)
vehicles.include_router(create)
vehicles.include_router(edit)
vehicles.include_router(view)
vehicles.include_router(deleted)
