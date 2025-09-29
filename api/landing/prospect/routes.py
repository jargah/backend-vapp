from fastapi import APIRouter, Depends
from .controller.register import register
from .controller.documentVehicle import vehicle
from .controller.documentDriver import driver
from .controller.photoVehicle import photo

from interceptors.credentials import Credentials

prospect = APIRouter(
    tags=['Landings - Prospect'], 
    prefix='/prospect', 
    dependencies=[
        Depends(Credentials(
            require_audience=True,
            require_issuer=True, 
            leeway=10
        )),
    ]
)
prospect.include_router(register)
prospect.include_router(vehicle)
prospect.include_router(photo)
prospect.include_router(driver)
