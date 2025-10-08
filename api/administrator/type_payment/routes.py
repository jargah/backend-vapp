from fastapi import APIRouter, Depends
from .controller.list import list
from .controller.create import create
from .controller.edit import edit
from .controller.view import view

from interceptors.session import Session
from interceptors.credentials import Credentials

typePayment = APIRouter(
    tags=['Administrator - Tipo Pago'], 
    prefix='/type-payment', 
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
typePayment.include_router(list)
typePayment.include_router(create)
typePayment.include_router(edit)
typePayment.include_router(view)
