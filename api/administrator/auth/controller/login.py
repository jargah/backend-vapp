from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db, rawDB
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.users import UsersModel
from helpers.response import ResponseHelper
from helpers.bcrypt import BCRYPT
from helpers.jwt import create


login = APIRouter()
@login.post("/login", 
    response_model=dict, 
    name='',
    
)
async def controller(request: Request, body: LoginDTO, db: Session = Depends(get_db)):
    try:

        mUser = UsersModel(db)   
        
        
        users = await mUser.selectFirst(
            "username = '{username}' AND active = 1".format(username=body.username)
        )
        
        print(users)
        
        if users == None:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_user_no_found']
            )
            
            
        if BCRYPT.verify(body.password, users['password']) == False:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_user_password_incorrect']
            )
        
        token = create({
            'id': users['id_user'],
            'rol_id': users['rol_id'],
            'username': users['username'],
            'phone': users['phone'],
            'email': users['email']
        })

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'token': token
            }
        )
        
    except Exception as e:
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )