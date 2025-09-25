from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database.MySQL import get_db
from helpers.response import ResponseHelper
from services.truora import createLink, getResult
from api.identity.dto.link import TruoraLinkDTO
from models.biometricResponse import BiometricResponseModel
from models.passengers import PassengersModel
from utils.datetime import now
from json import loads
from helpers.jwt import verify

webhook = APIRouter()
@webhook.post("/webhook", 
    response_model=dict, 
    name='',
)
async def controller(request: Request, db: Session = Depends(get_db)):
    try:
        
        mBiometricResponseModel = BiometricResponseModel(db)
        mPassengersModel = PassengersModel(db)

        raw = await request.body()
        result = raw.decode("utf-8", errors="replace")
        
        response_id = await mBiometricResponseModel.insert({
            'token': result,
            'creation': now()
        })
        
        data = verify(
            token=result, 
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
        
        print(data)
        
        mBiometricResponseModel = BiometricResponseModel(db)
        
        await mBiometricResponseModel.update(
            "id = '{id}'".format(id=response_id),
            {
                'process_id': data['object']['process_id'],
                'passenger_id': data['object']['metadata']['id_passenger'],
                'status': data['object']['status']
            }
        )
        
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
            data='OK'
        )
        
    except Exception as e:
        print(e)
        print('con')
        return ResponseHelper(
            code=400,
            message='Request failed',
            errors=['exception_controller']
        )