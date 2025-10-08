from api.administrator.type_motor.dto.type_motor import TypeMotorDTO
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from models.type_payment import TypePayment
from helpers.response import ResponseHelper
from utils.datetime import now



create = APIRouter()
@create.post("/create", 
    response_model=dict, 
    name='',
)
async def controller(dto: TypeMotorDTO, db: Session = Depends(get_db)):
    try:

        mTypePayment = TypePayment(db)
        
        check = await mTypePayment.selectFirst(
            "tipo_pago = '{name}'".format(name=dto.name)
        )
        
        if check != None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_type_payment_already_exist']
            )
            
        type_payment_data = {
            'tipo_pago': dto.name,
        }
            
        type_payment_id = await mTypePayment.insert(type_payment_data)
        if not type_payment_id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_create_type_motor']
            )
        

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'id': type_payment_id,
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