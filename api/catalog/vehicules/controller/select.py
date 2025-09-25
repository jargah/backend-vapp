from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from starlette.requests import Request
from models.vehicle import VehicleModel
from helpers.response import ResponseHelper

select = APIRouter()
@select.get("/select", 
    response_model=dict, 
    name='',
)
async def controller(db: Session = Depends(get_db)):
    try:

        mVehicule = VehicleModel(db)
        select = await mVehicule.selectAll('activo = 1', fields='id_vehiculo, nombre')
        
        if not select:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_vehicles_no_found']
            )
        

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'vehicles': select
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )