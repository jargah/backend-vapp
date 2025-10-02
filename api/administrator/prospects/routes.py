from fastapi import APIRouter, Depends
from .controller.list import list
from .controller.create import create
from .controller.edit import edit
from .controller.view import view
from .controller.delete import deleted
from interceptors.session import Session
from interceptors.credentials import Credentials

prospects = APIRouter(
    tags=['Administrator - Prospectos'], 
    prefix='/prospects', 
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
prospects.include_router(list)
prospects.include_router(create)
prospects.include_router(edit)
prospects.include_router(view)
prospects.include_router(deleted)
