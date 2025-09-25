from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.fleets_operators import FleetOperatorsModel
from helpers.response import ResponseHelper
from helpers.bcrypt import BCRYPT
from helpers.jwt import create

fleetList = APIRouter()


@fleetList.get("/", 
    response_model=dict, 
    name='',
    
)
async def controller(request: Request, db: Session = Depends(get_db)):
    try:

        mFleetGroup = FleetOperatorsModel(db)   
        
        
        fleets = await mFleetGroup.selectAll()
    
        if fleets == None:
            return ResponseHelper(
                code=400,
                errors={
                    'groups': [
                        'No se encontraron flotillas'
                    ]
                }
            )
        
        return ResponseHelper(
            code=200,
            data={
                'groups': fleets
            }
        )
        
    except Exception as e:
        print(str(e))
        return {
            'code': 400,
            'errors': ['exception_controller']
        }