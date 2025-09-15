from fastapi import APIRouter, Depends
from .controller.list import list
from .controller.create import create
from .controller.edit import edit
from .controller.view import view
from .controller.delete import deleted
from interceptors.session import Session
from interceptors.credentials import Credentials

roles = APIRouter(
    tags=['Administrator - Configuration - Roles'], 
    prefix='/configuration/roles', 
    dependencies=[
        Depends(Credentials(
            require_audience=True,
            require_issuer=True, 
            leeway=10
        )),
        Depends(Session())
    ]
)
roles.include_router(list)
roles.include_router(create)
roles.include_router(edit)
roles.include_router(view)
roles.include_router(deleted)
