from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db, rawDB
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.administrator import AdministratorModel
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

        mUser = AdministratorModel(db)   
        
        
        users = await mUser.selectFirst(
            "username = '{username}' AND active = 1".format(username=body.username)
        )
        

        if users == None:
            return ResponseHelper(
                code=400,
                errors={
                    'users': [
                        'El usuario no se encontro'
                    ]
                }
            )
        
        token = create({
            'id': users['id'],
            'rol_id': users['rol_id'],
            'username': users['username'],
            'phone': users['phone'],
            'email': users['email']
        })

        return ResponseHelper(
            code=200,
            data={
                'session': token
            }
        )
        
    except Exception as e:
        print(str(e))
        return {
            'code': 400,
            'errors': ['exception_controller']
        }