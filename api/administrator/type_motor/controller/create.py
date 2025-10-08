from api.administrator.type_motor.dto.type_motor import TypeMotorDTO
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from models.type_motor import TypeMotor
from helpers.response import ResponseHelper
from utils.datetime import now



create = APIRouter()
@create.post("/create", 
    response_model=dict, 
    name='',
)
async def controller(dto: TypeMotorDTO, db: Session = Depends(get_db)):
    try:

        mTypeMotor = TypeMotor(db)
        
        check = await mTypeMotor.selectFirst(
            "nombre_tipo_motor = '{name}'".format(name=dto.name)
        )
        
        if check != None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_vehicle_already_exist']
            )
            
        type_motor_data = {
            'nombre_tipo_motor': dto.name,
        }
            
        type_motor_id = await mTypeMotor.insert(type_motor_data)
        if not type_motor_id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_create_type_motor']
            )
        

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'id': type_motor_id,
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