from fastapi import APIRouter, Depends

from api.catalog.vehicules.routes import vehicle

catalog = APIRouter(
    prefix='/catalog'
)

catalog.include_router(vehicle)
