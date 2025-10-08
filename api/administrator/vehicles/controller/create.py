from api.administrator.vehicles.dto.vehicle import VehicleDTO
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from models.vehicle import VehicleModel
from helpers.response import ResponseHelper
from utils.datetime import now



create = APIRouter()
@create.post("/create", 
    response_model=dict, 
    name='',
)
async def controller(dto: VehicleDTO, db: Session = Depends(get_db)):
    try:

        mVehicleModel = VehicleModel(db)
        
        check = await mVehicleModel.selectFirst(
            "nombre = '{name}' AND activo = 1".format(name=dto.name)
        )
        
        if check != None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_vehicle_already_exist']
            )
            
        print(dto)
            
        vehicle_data = {
            'nombre': dto.name,
            'marca': dto.branch,
            'modelo': dto.model_,
            'activo': True
        }
        
        print(vehicle_data)
        
            
        vehicle_id = await mVehicleModel.insert(vehicle_data)
        if not vehicle_id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_create_user']
            )
        

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'id': vehicle_id,
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