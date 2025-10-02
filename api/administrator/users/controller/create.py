from api.administrator.users.dto.user import UserDTO
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from models.users import UsersModel
from helpers.response import ResponseHelper
from utils.datetime import now
from helpers.bcrypt import BCRYPT



create = APIRouter()
@create.post("/create", 
    response_model=dict, 
    name='',
)
async def controller(dto: UserDTO, db: Session = Depends(get_db)):
    try:

        mUser = UsersModel(db)
        
        check = await mUser.selectFirst(
            "email = '{email}' AND active = 1".format(email=dto.email)
        )
        
        if check != None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_user_already_exist']
            )
            
        user_data = {
            **dto.model_dump(),
            **{
                'active': True,
                'creation': now()
            }
        }
        
        user_data['password'] = BCRYPT.hash(user_data['password'])
        
            
        user_id = await mUser.insert(user_data)
        if not user_id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_create_user']
            )
        

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'id': user_id,
                'created': True
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )