from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db, rawDB
from api.administrator.fleets.dto.fleets import ViewFleetDTO
from starlette.requests import Request
from models.fleets import FleetsModel
from helpers.response import ResponseHelper
from helpers.bcrypt import BCRYPT
from helpers.jwt import create

configView = APIRouter()


@configView.get("/{id}", 
    response_model=dict, 
    name='',
    
)
async def controller(params: ViewFleetDTO = Depends(), db: Session = Depends(get_db)):
    try:
        
        if not params.id:
            return ResponseHelper(
                code=400,
                errors={
                    'fleets': [
                        'error_id_required'
                    ]
                }
            )
        
        mFleets = FleetsModel(db)   
        
        fleets = await mFleets.selectFirst(
            "id = '{id}' AND active = 1".format(id=params.id)
        )
        

        if fleets == None:
            return ResponseHelper(
                code=400,
                errors={
                    'fleets': [
                        'error_no_found_fleet'
                    ]
                }
            )
    

        return ResponseHelper(
            code=200,
            data={
                'fleet': fleets
            }
        )
        
    except Exception as e:
        print(str(e))
        return {
            'code': 400,
            'errors': ['exception_controller']
        }