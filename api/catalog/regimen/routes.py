from fastapi import APIRouter, Depends
from .controller.select import select

from interceptors.credentials import Credentials

regimen = APIRouter(
    tags=['Catalog - REgimen'], 
    prefix='/regimen', 
    dependencies=[
        Depends(Credentials(
            require_audience=True,
            require_issuer=True, 
            leeway=10
        )),
    ]
)
regimen.include_router(select)
