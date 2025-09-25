from fastapi import APIRouter, Depends
from .controller.select import select

from interceptors.credentials import Credentials

vehicle = APIRouter(
    tags=['Catalog - Vehicle'], 
    prefix='/vehicle', 
    dependencies=[
        Depends(Credentials(
            require_audience=True,
            require_issuer=True, 
            leeway=10
        )),
    ]
)
vehicle.include_router(select)
