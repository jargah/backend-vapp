from fastapi import APIRouter, Depends
from .controller.list import list
from .controller.create import create
from .controller.edit import edit
from .controller.view import view
from .controller.delete import deleted

from interceptors.session import Session
from interceptors.credentials import Credentials

taxi = APIRouter(
    tags=['Administrator - Taxi'], 
    prefix='/taxi', 
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
taxi.include_router(list)
taxi.include_router(create)
taxi.include_router(edit)
taxi.include_router(view)
taxi.include_router(deleted)
