from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from api.administrator.referral_benefits.dto.referral import CreateBenefitsDTO
from starlette.requests import Request
from models.referral_benefits import ReferralBenefitModel
from helpers.response import ResponseHelper
from helpers.dates import now_formatted
from helpers.jwt import create

referralCreate = APIRouter()


@referralCreate.post("/", 
    response_model=dict, 
    name='',
    
)
async def controller(request: Request, body: CreateBenefitsDTO, db: Session = Depends(get_db)):
    try:

        mReferralBenefit = ReferralBenefitModel(db)   
        
        benefits = await mReferralBenefit.selectFirst(
            "name = '{email}' AND active = '1' ".format(name=body.name)
        )
        
        
        if benefits != None and benefits['active'] :
            return ResponseHelper(
                code=400,
                errors={
                    'fleet': [
                        'fleet_already_exist'
                    ]
                }
            )
            
        
 
        fleet_data = body.model_dump()
        fleet_data['active'] = True
        fleet_data['creation'] = now_formatted()
        
        
        benefits_id = await mReferralBenefit.insert(fleet_data)
        
        if benefits_id == 0:
            return ResponseHelper(
                code=400,
                errors={
                    'fleet': [
                        'error_create_fleet'
                    ]
                }
            )
        

        return ResponseHelper(
            code=200,
            data={
                'benefits': {
                    'id': benefits_id
                }
            }
        )
        
    except Exception as e:
        print(str(e))
        return {
            'code': 400,
            'errors': ['exception_controller']
        }