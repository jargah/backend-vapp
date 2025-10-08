from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.passengers import PassengersModel
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

        mPassengersModel = PassengersModel(db)
        passenger = await mPassengersModel.view(id=id)
        
        if passenger == None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_passenger_no_found']
            )
            
        data = {
            "passenger": {
                "id": passenger.get("id"),
                "first_name": passenger.get("first_name"),
                "last_name": passenger.get("last_name"),
                "second_surname": passenger.get("second_surname"),
                "phone": passenger.get("phone"),
                "username": passenger.get("username"),
                "email": passenger.get("email"),
                "zipcode_passenger": passenger.get("zipcode_passenger"),
                "gender": passenger.get("gender"),
                "register_date": passenger.get("register_date"),
            },
            "fiscal": {
                "zipcode_fiscal": passenger.get("zipcode_fiscal"),
                "tax": passenger.get("tax"),
                "taxid": passenger.get("taxid"),
            },
            "metrics": {
                "score": passenger.get("score"),
                "facial_verification": False if not passenger.get("facial_verification") else True,
            }
        }
            
        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data=data
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )