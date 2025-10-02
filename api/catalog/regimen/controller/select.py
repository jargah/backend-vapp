from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from starlette.requests import Request
from models.regimen import RegimenModel
from helpers.response import ResponseHelper

select = APIRouter()
@select.get("/select", 
    response_model=dict, 
    name='',
)
async def controller(db: Session = Depends(get_db)):
    try:

        mRegimenModel = RegimenModel(db)
        select = await mRegimenModel.selectAll('')
        
        if not select:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_vehicles_no_found']
            )
        

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'regimen': select
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )