from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.fleets import FleetsModel
from helpers.response import ResponseHelper
from helpers.bcrypt import BCRYPT
from helpers.jwt import create

configList = APIRouter()


@configList.get("/", 
    response_model=dict, 
    name='',
    
)
async def controller(request: Request, db: Session = Depends(get_db)):
    try:

        mUser = FleetsModel(db)   
        
        
        fleets = await mUser.featchAllRows()
    
        if fleets == None:
            return ResponseHelper(
                code=400,
                errors={
                    'fleets': [
                        'No se encontraron flotillas'
                    ]
                }
            )
        
        return ResponseHelper(
            code=200,
            data={
                'fleets': fleets
            }
        )
        
    except Exception as e:
        print(str(e))
        return {
            'code': 400,
            'errors': ['exception_controller']
        }