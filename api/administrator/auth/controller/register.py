from fastapi import APIRouter, Depends, HTTPException
from schemas.account.login import AccountLoginSchema

register = APIRouter()
@register.post(
    "/register", 
    response_model=dict, 
    name=''
)
async def loginUser(body: AccountLoginSchema):
    return {}