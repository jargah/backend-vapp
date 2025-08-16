from fastapi import APIRouter, Depends, HTTPException
from schemas.account.login import AccountLoginSchema

recovery = APIRouter()
@recovery.post("/recovery", response_model=dict, name='')
async def loginUser(body: AccountLoginSchema):
    return {}