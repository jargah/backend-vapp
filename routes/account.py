from fastapi import APIRouter

from api.account.login import router as account

account = APIRouter(
    tags=['Account'],
    prefix='/account'
)