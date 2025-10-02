from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.users import UsersModel
from models.users_session import UserSessionModel
from helpers.response import ResponseHelper
from helpers.bcrypt import BCRYPT
from helpers.jwt import create
from uuid import uuid4
from utils.datetime import now

login = APIRouter()
@login.post("/login", 
    response_model=dict, 
    name='',
    
)
async def controller(request: Request, body: LoginDTO, db: Session = Depends(get_db)):
    try:

        mUser = UsersModel(db)   
        mUserSessionModel = UserSessionModel(db)
        
        users = await mUser.selectFirst(
            "username = '{username}' AND active = 1".format(username=body.username)
        )
        
        uid = uuid4()
        
        if users == None:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_user_no_found']
            )
            
        print(BCRYPT.hash(body.password))
            
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
        }, expires_minutes=60)
        

        if token == None:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=[token['error']]
            )
            
        await mUserSessionModel.update(
            "user_id = '{user_id}'".format(user_id=users['id_user']),
            { 'active': False }
        )
            
        await mUserSessionModel.insert({
            'user_id': users['id_user'],
            'appid': str(uid),
            'token': str(token),
            'active': True,
            'creation': now()
        })
            
        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'appid': uid,
                'token': token
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )