from fastapi import APIRouter, Depends
from helpers.jwt import verify
from sqlalchemy.orm import Session
from database.MySQL import get_db
from helpers.response import ResponseHelper
from services.truora import createLink, getResult
from api.identity.dto.link import TruoraLinkDTO
from models.biometricLink import BiometricLinkModel
from models.biometricResponse import BiometricResponseModel
from models.passengers import PassengersModel
from utils.datetime import now
from json import dumps

check = APIRouter()
@check.get("/check/{id}", 
    response_model=dict, 
    name='',
)
async def controller(id: str, db: Session = Depends(get_db)):
    try:
        
        mBiometricResponseModel = BiometricResponseModel(db)
        mPassengersModel = PassengersModel(db)

        if not id:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_empty_id_required']
            )
        
        find = await mBiometricResponseModel.selectFirst(
            "process_id = '{process_id}'".format(process_id=id),
            'DESC'
        )
        
        if not find:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_process_id_no_found']
            )
             
        biometric = getResult(id)
        

        if biometric['error'] == True:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['error_biometric_no_found']
            )
            
 
        biometric_result = biometric['data']
        
        data = verify(
            token=find['token'], 
            algorithms=['HS256'],
            key="42e548a7e5a34161b425f7a94fde2c0be81ff2c6628fc1eaa517878455a268e4"
        )
        
        if not data:
            return ResponseHelper(
                code=400,
                message='Request failed',
                errors=['troura_token_invalid']
            )
            
            
        data = data['payload']['events'][len(data['payload']['events']) - 1]
        
        if data['object']['status'] == 'success':
        
            user_verify = await mPassengersModel.selectFirst(
                "id_pasajero = '{id_pasajero}'".format(id_pasajero=data['object']['metadata']['id_passenger'])
            )
            
            if not user_verify:
                return ResponseHelper(
                    code=400,
                    message='Request failed',
                    errors=['error_passenger_no_found']
                )
                
            validate_user = await mPassengersModel.update(
                "id_pasajero = '{id_pasajero}'".format(id_pasajero=data['object']['metadata']['id_passenger']),
                {
                    'verificacion_facial': 1
                }
            )
        
            if not validate_user:
                return ResponseHelper(
                    code=400,
                    message='Request failed',
                    errors=['error_passenger_no_found']
                )

        return ResponseHelper(
            code=200,
            message='Request completed successfully',
            data={
                'status': biometric_result['status'],
                'id': id
            }
        )
        
    except Exception as e:
        print(e)
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )