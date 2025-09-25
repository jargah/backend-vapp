from fastapi import APIRouter, Depends

from api.landing.prospect.routes import prospect

landing = APIRouter(
    prefix='/landing'
)

landing.include_router(prospect)
