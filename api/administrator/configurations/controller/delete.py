from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db, rawDB
from api.administrator.fleets.dto.fleets import UpdateFleetDTO
from starlette.requests import Request
from models.fleets import FleetsModel
from helpers.response import ResponseHelper
from helpers.bcrypt import BCRYPT
from helpers.jwt import create

configDelete = APIRouter()


@configDelete.delete("/{id}", 
    response_model=dict, 
    name='',
    
)
async def controller(id: int, db: Session = Depends(get_db)):
    try:

        if not id:
            return ResponseHelper(
                code=400,
                errors={
                    'fleets': [
                        'error_id_required'
                    ]
                }
            )
            

        mFleets = FleetsModel(db)   
        
        fleet = await mFleets.selectFirst(
            "id = '{id}' AND active = 1".format(id=id)
        )
        
        if fleet == None:
            return ResponseHelper(
                code=400,
                errors={
                    'fleet': [
                        'fleet_no_exist'
                    ]
                }
            )
            
        update_fleet = await mFleets.update(
            "id = '{id}'".format(id=id),
            {
                'active': False
            }
        )
        
        
        if update_fleet == 0:
            return ResponseHelper(
                code=400,
                errors={
                    'fleet': [
                        'error_update_fleet'
                    ]
                }
            )
        

        return ResponseHelper(
            code=200,
            data={
                'fleet': {
                    'delete': True,
                    'id': id,
                }
            }
        )
        
    except Exception as e:
        print(str(e))
        return {
            'code': 400,
            'errors': ['exception_controller']
        }