from api.administrator.vehicles.dto.vehicle import VehicleDTO
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.vehicle import VehicleModel
from helpers.response import ResponseHelper
from schemas.datatable import DataTableQueryDTO, datatable_query_dependency
from utils.datetime import now



edit = APIRouter()
@edit.put("/{id}/edit", 
    response_model=dict, 
    name='',
)
async def controller(id: int, dto: VehicleDTO, db: Session = Depends(get_db)):
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
                errors=['error_user_no_found']
            )
            
        vehicle_data = {
            'nombre': dto.name,
            'marca': dto.branch,
            'modelo': dto.model_
        }
        
        
        user_id = await mVehicleModel.update(
            "id_vehiculo = '{id}'".format(id=id),
            data=vehicle_data
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