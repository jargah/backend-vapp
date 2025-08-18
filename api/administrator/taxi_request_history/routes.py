from fastapi import APIRouter, Depends
from interceptors.token import Token
from interceptors.credentials import Credentials

from .controller.list import taxiList
from .controller.create import taxiCreate
from .controller.update import taxiUpdate
from .controller.view import taxiView
from .controller.delete import taxiDelete

taxi = APIRouter(
    tags=['Administrator Taxi Request History'], 
    prefix='/taxi-request-history', 
    dependencies=[
        Depends(Token()),
        Depends(Credentials())
    ]
)
taxi.include_router(taxiList)
taxi.include_router(taxiCreate)
taxi.include_router(taxiUpdate)
taxi.include_router(taxiView)
taxi.include_router(taxiDelete)
