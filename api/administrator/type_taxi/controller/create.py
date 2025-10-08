from api.administrator.type_motor.dto.type_motor import TypeMotorDTO
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from models.type_taxi import TypeTaxi
from helpers.response import ResponseHelper
from utils.datetime import now



create = APIRouter()
@create.post("/create", 
    response_model=dict, 
    name='',
)
async def controller(dto: TypeMotorDTO, db: Session = Depends(get_db)):
    try:

        mTypeTaxi = TypeTaxi(db)
        
        check = await mTypeTaxi.selectFirst(
            "nombre_tipo_taxi = '{name}'".format(name=dto.name)
        )
        
        if check != None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_type_taxi_already_exist']
            )
            
        type_taxi_data = {
            'nombre_tipo_taxi': dto.name,
        }
            
        type_taxi_id = await mTypeTaxi.insert(type_taxi_data)
        if not type_taxi_id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_create_type_taxi']
            )
        

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'id': type_taxi_id,
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