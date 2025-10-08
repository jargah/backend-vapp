from fastapi import APIRouter, Depends
from .controller.list import list
from .controller.view import view

from interceptors.session import Session
from interceptors.credentials import Credentials

service = APIRouter(
    tags=['Administrator - Servicio'], 
    prefix='/service-travel', 
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
service.include_router(list)
service.include_router(view)
