from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.vehicle import VehicleModel
from helpers.response import ResponseHelper
from schemas.datatable import DataTableQueryDTO, datatable_query_dependency



view = APIRouter()
@view.get("/{id}/view", 
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
        check = await mVehicleModel.view(id=id)
        
        if check == None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_vehicle_no_found']
            )
            
        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data=check
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )