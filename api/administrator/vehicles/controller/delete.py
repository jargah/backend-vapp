from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.vehicle import VehicleModel
from helpers.response import ResponseHelper
from schemas.datatable import DataTableQueryDTO, datatable_query_dependency



deleted = APIRouter()
@deleted.delete("/{id}/delete", 
    response_model=dict, 
    name='',
)
async def controller(id: int, db: Session = Depends(get_db)):
    try:

        if not id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_empty_id']
            )

        mVehicleModel = VehicleModel(db)
        check = await mVehicleModel.selectFirst(
            "id_vehiculo = '{id}' AND activo = 1".format(id=id)
        )
        

        if check == None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_vehicle_no_found']
            )
            
        
        
        
        user_id = await mVehicleModel.update(
            "id_vehiculo = '{id}'".format(id=id),
            data={
                'activo': False
            }
        )
        
        if not user_id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_create_user']
            )
        

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'id': id,
                'deleted': True
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )