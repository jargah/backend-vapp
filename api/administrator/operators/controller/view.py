from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.operators import OperatorsModel
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

        mOperators = OperatorsModel(db)
        operator = await mOperators.view(id=id)
        
        if operator == None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_operator_no_found']
            )
            
        g = operator.get
            
        data = {
            "operator": {
                "id": g("id"),
                "first_name": g("first_name"),
                "last_name": g("last_name"),
                "second_surname": g("second_surname"),
                "username": g("username") or g("phone"),
                "phone": g("phone"),
                "email": g("email"),
                "email_verify": g("email_verify"),
                "picture": g("picture") or "",
                "taxid": g("taxid"),
                "curp": g("curp"),
                "gender": g("gender"),
                "birthday": g("birthday"),
                "address": g("address"),
                "suburb": g("suburb"),
                "zipcode": g("zipcode"),
                "state": g("state"),
                "municipality": g("municipality"),
                "empresa_operador": {
                    "id": g("empresa_operador_id"),
                    "name": g("empresa_operador"),
                },
                "register_date": g("register_date"),
            },
            "taxi": {
                "empresa": {
                    "id": g("taxi_empresa_id"),
                    "name": g("taxi_empresa"),
                },
                "branch": g("branch"),
                "sub_branch": g("sub_branch"),
                "model": g("model"),
                "number_eco": g("number_eco"),
                "number_plate": g("number_plate"),
                "serie": g("serie"),
                "type_taxi": {
                    "id": g("type_taxi_id"),
                    "name": g("type_taxi"),
                },
                "type_motor": {
                    "id": g("type_motor_id"),
                    "name": g("type_motor"),
                },
            },
            "balance": {
                "total": g("balance"),
                "pending": g("balance_pending"),
                "invoice": g("balance_invoice"),
            },
            "metrics": {
                "score": g("score"),
                "travels": int(g("travels")) if g("travels") is not None else None,
            },
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