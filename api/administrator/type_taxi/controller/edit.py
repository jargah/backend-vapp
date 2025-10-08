from api.administrator.type_motor.dto.type_motor import TypeMotorDTO
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.type_taxi import TypeTaxi
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

        mTypeTaxi = TypeTaxi(db)
        check = await mTypeTaxi.selectFirst(
            "id_tipo_taxi = '{id}'".format(id=id)
        )
        

        if check == None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_type_taxi_no_found']
            )
            
        type_taxi_data = {
            'nombre_tipo_taxi': dto.name,
        }
        
        
        type_motor_id = await mTypeTaxi.update(
            "id_tipo_taxi = '{id}'".format(id=id),
            data=type_taxi_data
        )
        
        if not type_motor_id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_update_type_taxi']
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