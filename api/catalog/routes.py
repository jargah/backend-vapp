from fastapi import APIRouter, Depends

from api.catalog.vehicules.routes import vehicle
from api.catalog.regimen.routes import regimen

catalog = APIRouter(
    prefix='/catalog'
)

catalog.include_router(vehicle)
catalog.include_router(regimen)
