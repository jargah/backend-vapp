from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Any, Iterable, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.prospect import PropectModel
from models.prospect_vehicle import ProspectVehicleModel
from models.prospect_document import ProspectDocumentModel
from helpers.response import ResponseHelper
from schemas.datatable import DataTableQueryDTO, datatable_query_dependency
from helpers.AWSS3 import AwsStorage
import re


view = APIRouter()
@view.get("/{id}/view", 
    response_model=dict, 
    name='',
)
async def controller(id: int, db: Session = Depends(get_db)):
    
    s3 = AwsStorage()
    
    try:
        
        if not id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_empty_id']
            )

        mPropectModel = PropectModel(db)
        mProspectVehicleModel = ProspectVehicleModel(db)
        mProspectDocumentModel = ProspectDocumentModel(db)
        
        check = await mPropectModel.selectFirst(
            "id_prospecto = '{id}' AND activo = 1".format(id=id)
        )
        

        if check == None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_prospect_no_found']
            )
            
        data = {
            'prospect': check,
            'vehicles': None,
            'documents': {}
        }
        
        data['vehicles'] = await mProspectVehicleModel.selectAll(
            "id_prospecto = '{id}'".format(id=id)
        )
        
        documents = await mProspectDocumentModel.selectFirst(
            "prospecto_id = '{id}'".format(id=id),
            fields='tarjeta_circulacion,poliza_seguro,factura,calcomania_verificacion,foto_frontal_vehiculo,foto_atras_vehiculo,foto_derecho_vehiculo,foto_izquierdo_vehiculo,foto_vehiculo,constancia_fiscal,ine_frontal,ine_atras,csd_certificado,csd_llave,rfc,regimen'
        )
        
        pattern = re.compile(
            r"document/(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12})(?=$|[/?#])"
        )
        
        if documents != None:
            for key in documents:
                
                if key != 'rfc' and key != 'regimen':
                    file = s3.generate_url('documentos-prospectos', documents[key])
                    data['documents'][key] = file
                else:
                    data['documents'][key]  = documents[key]
        
        
            
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
        