from fastapi import APIRouter, Depends
from interceptors.token import Token
from interceptors.credentials import Credentials

from .controller.list import configList
from .controller.create import configCreate
from .controller.update import configUpdate
from .controller.view import configView
from .controller.delete import configDelete

configurations = APIRouter(
    tags=['Administrator Configurations'], 
    prefix='/configurations', 
    dependencies=[
        Depends(Token()),
        Depends(Credentials())
    ]
)
configurations.include_router(configList)
configurations.include_router(configCreate)
configurations.include_router(configUpdate)
configurations.include_router(configView)
configurations.include_router(configDelete)
