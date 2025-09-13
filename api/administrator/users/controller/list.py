from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db, rawDB
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.users import UsersModel
from helpers.response import ResponseHelper
from schemas.datatable import DataTableQueryDTO, datatable_query_dependency



list = APIRouter()
@list.get("/list", 
    response_model=dict, 
    name='',
)
async def controller(request: Request, query: Annotated[DataTableQueryDTO, Depends(datatable_query_dependency)], db: Session = Depends(get_db)):
    try:

        mUser = UsersModel(db)
        datatable = await mUser.list(query.database, query.page, query.rows, query.search, query.order_by, query.order_asc)
    

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'users': datatable
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )