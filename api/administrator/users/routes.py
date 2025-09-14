from fastapi import APIRouter, Depends
from .controller.list import list
from .controller.create import create
from .controller.edit import edit
from .controller.view import view
from .controller.delete import deleted
from interceptors.session import Session
from interceptors.credentials import Credentials

users = APIRouter(
    tags=['Administrator - Configuration - Users'], 
    prefix='/configuration/users', 
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
users.include_router(list)
users.include_router(create)
users.include_router(edit)
users.include_router(view)
users.include_router(deleted)
