from fastapi import APIRouter, HTTPException
from schemas.account.login import AccountLoginSchema
from starlette.requests import Request
from models.account.users import UserModel
import json

login = APIRouter()
@login.post("/login", 
    response_model=dict, 
    name='',
    
)
async def controller(request: Request, body: AccountLoginSchema):
    try:

        db = request.state.mysql

        mUser = UserModel(db)   
        users = await mUser.selectFirst()

        return {
            'data': users
        }
    except Exception as e:
        print(str(e))
        return {
            'code': 400,
            'errors': ['exception_controller']
        }