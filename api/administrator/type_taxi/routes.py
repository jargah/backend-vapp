from fastapi import APIRouter, Depends
from .controller.list import list
from .controller.create import create
from .controller.edit import edit
from .controller.view import view

from interceptors.session import Session
from interceptors.credentials import Credentials

typeTaxi = APIRouter(
    tags=['Administrator - Tipo axi'], 
    prefix='/type-taxi', 
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
typeTaxi.include_router(list)
typeTaxi.include_router(create)
typeTaxi.include_router(edit)
typeTaxi.include_router(view)
