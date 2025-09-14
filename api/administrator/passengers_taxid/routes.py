from fastapi import APIRouter, Depends
from interceptors.session import Session
from interceptors.credentials import Credentials

from .controller.list import passengersList
from .controller.create import passengersCreate
from .controller.update import passengersUpdate
from .controller.view import passengersView
from .controller.delete import passengersDelete

passengers = APIRouter(
    tags=['Administrator Passengers TaxId'], 
    prefix='/passengers-taxid', 
    dependencies=[
        Depends(Session()),
        Depends(Credentials())
    ]
)
passengers.include_router(passengersList)
passengers.include_router(passengersCreate)
passengers.include_router(passengersUpdate)
passengers.include_router(passengersView)
passengers.include_router(passengersDelete)
