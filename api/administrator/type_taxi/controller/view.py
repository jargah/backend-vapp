from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.type_taxi import TypeTaxi
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

        mTypeTaxi = TypeTaxi(db)
        check = await mTypeTaxi.view(id=id)
        
        if check == None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_type_taxi_no_found']
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