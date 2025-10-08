from api.administrator.type_motor.dto.type_motor import TypeMotorDTO
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.type_payment import TypePayment
from helpers.response import ResponseHelper
from schemas.datatable import DataTableQueryDTO, datatable_query_dependency
from utils.datetime import now



edit = APIRouter()
@edit.put("/{id}/edit", 
    response_model=dict, 
    name='',
)
async def controller(id: int, dto: TypeMotorDTO, db: Session = Depends(get_db)):
    try:

        if not id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_empty_id']
            )

        mTypePayment = TypePayment(db)
        check = await mTypePayment.selectFirst(
            "id_tipo_pago = '{id}'".format(id=id)
        )
        

        if check == None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_type_payment_no_found']
            )
            
        vehicle_data = {
            'tipo_pago': dto.name,
        }
        
        
        type_motor_id = await mTypePayment.update(
            "id_tipo_pago = '{id}'".format(id=id),
            data=vehicle_data
        )
        
        if not type_motor_id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_update_type_payment']
            )
        

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'id': id,
                'updated': True
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )