from fastapi import APIRouter, Request
from schemas.account.login import AccountLoginSchema
from fastapi.security.base import SecurityBase
from typing import Annotated

login = APIRouter()
@login.post("/login", 
    response_model=dict, 
    name='login',
)
async def loginUser(request: Request, body: AccountLoginSchema):

    print(body)

    print(f'request => {request}')
    return {}