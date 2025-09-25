from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.MySQL import get_db
from helpers.response import ResponseHelper
from services.truora import createLink, getResult
from api.identity.dto.link import TruoraLinkDTO
from models.biometricLink import BiometricLinkModel
from utils.datetime import now
from json import dumps

link = APIRouter()
@link.post("/link", 
    response_model=dict, 
    name='',
)
async def controller(dto: TruoraLinkDTO, db: Session = Depends(get_db)):
    try:
        

        json = dto.model_dump()
        prepareLink = createLink(json)

        if prepareLink['error'] == True:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_created_biometric_validation']
            )

        truora = prepareLink['data']
        mBiometricLinkModel = BiometricLinkModel(db)
        
    
        link_data = {
            'body': dumps(json),
            'url': truora['process_link'],
            'token': truora['token'],
            'process_id': truora['process_id'],
            'creation': now()
        }
        
        link_id = await mBiometricLinkModel.insert(link_data)
        if not link_id or link_id == 0:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_creation_url']
            )
            
        

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'link': truora['process_link'],
                'process_id': truora['process_id']
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )