from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from api.administrator.fleets.dto.fleets import UpdateFleetDTO
from models.fleets import FleetsModel
from helpers.response import ResponseHelper
from helpers.bcrypt import BCRYPT
from helpers.jwt import create

configUpdate = APIRouter()


@configUpdate.put("/{id}", 
    response_model=dict, 
    name='',
    
)
async def controller(id: int, body: UpdateFleetDTO, db: Session = Depends(get_db)):
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
        
        if fleet != None:
            return ResponseHelper(
                code=400,
                errors={
                    'fleet': [
                        'fleet_already_exist'
                    ]
                }
            )
            
        update_fleet = await mFleets.update(
            "id = '{id}'".format(id=id),
            body.model_dump()
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
                    'update': True,
                    'id': id,
                    'email': body.email
                }
            }
        )
        
    except Exception as e:
        print(str(e))
        return {
            'code': 400,
            'errors': ['exception_controller']
        }