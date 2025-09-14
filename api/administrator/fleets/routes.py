from fastapi import APIRouter, Depends
from interceptors.session import Session
from interceptors.credentials import Credentials

from .controller.list import fleetList
from .controller.create import fleetCreate
from .controller.update import fleetUpdate
from .controller.view import fleetView
from .controller.delete import fleetDelete

fleets = APIRouter(
    tags=['Administrator Fleets'], 
    prefix='/fleets', 
    dependencies=[
        Depends(Session()),
        Depends(Credentials())
    ]
)
fleets.include_router(fleetList)
fleets.include_router(fleetCreate)
fleets.include_router(fleetUpdate)
fleets.include_router(fleetView)
fleets.include_router(fleetDelete)
