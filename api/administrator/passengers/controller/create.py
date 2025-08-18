from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db, rawDB
from api.administrator.fleets.dto.fleets import CreateFleetDTO
from starlette.requests import Request
from models.fleets import FleetsModel
from helpers.response import ResponseHelper
from helpers.dates import now_formatted
from helpers.jwt import create

passengersCreate = APIRouter()


@passengersCreate.post("/", 
    response_model=dict, 
    name='',
    
)
async def controller(request: Request, body: CreateFleetDTO, db: Session = Depends(get_db)):
    try:

        mFleets = FleetsModel(db)   
        
        fleet = await mFleets.selectFirst(
            "email = '{email}' AND active = '1' ".format(email=body.email)
        )
        
        
        if fleet != None and fleet['active'] :
            return ResponseHelper(
                code=400,
                errors={
                    'fleet': [
                        'fleet_already_exist'
                    ]
                }
            )
            
        
 
        fleet_data = body.model_dump()
        fleet_data['active'] = True
        fleet_data['creation'] = now_formatted()
        
        
        fleet_id = await mFleets.insert(fleet_data)
        
        if fleet_id == 0:
            return ResponseHelper(
                code=400,
                errors={
                    'fleet': [
                        'error_create_fleet'
                    ]
                }
            )
        

        return ResponseHelper(
            code=200,
            data={
                'fleet': {
                    'id': fleet_id
                }
            }
        )
        
    except Exception as e:
        print(str(e))
        return {
            'code': 400,
            'errors': ['exception_controller']
        }