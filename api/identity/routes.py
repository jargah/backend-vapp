from fastapi import APIRouter, Depends
from .controller.link import link
from .controller.webhook import webhook
from .controller.check import check

from interceptors.credentials import Credentials

identity = APIRouter(
    tags=['Identity'], 
    prefix='/identity', 
    dependencies=[
        Depends(Credentials(
            require_audience=True,
            require_issuer=True, 
            leeway=10
        )),
    ]
)
identity.include_router(link)
identity.include_router(webhook)
identity.include_router(check)
