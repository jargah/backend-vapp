from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.users import UsersModel
from models.roles import RolesModel
from models.users_session import UserSessionModel
from helpers.response import ResponseHelper
from helpers.bcrypt import BCRYPT
from helpers.jwt import create
from uuid import uuid4
from utils.datetime import now

me = APIRouter()
@me.get("/me", 
    response_model=dict, 
    name='',
    
)
async def controller(request: Request, db: Session = Depends(get_db)):
    try:

        mUser = UsersModel(db)   
        mRolesModel = RolesModel(db)
        mUserSessionModel = UserSessionModel(db)
        
        session = request.state.session
    
        checkSession = await mUserSessionModel.selectFirst(
            "user_id = '{id}'".format(id=session['id'])
        )        
        
        if not checkSession:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_session_no_found']
            )
            
        role = await mRolesModel.selectFirst("id_role = '{id_role}'".format(id_role=session['rol_id']))
        if not role:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_no_found_role']
            )
            
        session['role_name'] = role['name']
        
           
        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'me': session,
                'token': checkSession['token']
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )