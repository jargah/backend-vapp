from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.roles import RolesModel
from helpers.response import ResponseHelper
from schemas.datatable import DataTableQueryDTO, datatable_query_dependency

select = APIRouter()
@select.get("/select", 
    response_model=dict, 
    name='',
)
async def controller(db: Session = Depends(get_db)):
    try:

        mRolesModel = RolesModel(db)
        roles = await mRolesModel.selectAll(fields='id_role,name')
    

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'roles': roles
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )