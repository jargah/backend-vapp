from fastapi import APIRouter, Depends
from .controller.register import register

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
