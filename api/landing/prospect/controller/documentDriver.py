from __future__ import annotations
from uuid import uuid4

from fastapi import APIRouter, Depends
from helpers.AWSS3 import AwsStorage
from sqlalchemy.engine import Connection

from database.MySQL import get_db, ensure_tx, commit_tx, rollback_tx
from api.landing.prospect.dto.documentDriver import DocumentDriverDTO
from models.prospect import PropectModel
from models.prospect_document import ProspectDocumentModel
from helpers.response import ResponseHelper
from utils.globals import calculate_max_bytes, get_full_extension, size_guard, split_fullname
from utils.datetime import now

fields = {
    'tax_certificate': 'constancia_fiscal',
    'ine_front': 'ine_frontal',
    'ine_back': 'ine_atras',
    'csd_certificate': 'csd_certificado',
    'csd_key': 'csd_llave',
    'csd_password': 'csd_clave',
    'taxid': 'rfc',
    'regimen': 'regimen',
}

driver = APIRouter()

@driver.post(
    "/{id}/document-fiscal", 
    response_model=dict,
    name=""
)
async def controller(id: int, payload: DocumentDriverDTO = Depends(DocumentDriverDTO.as_form), conn: Connection = Depends(get_db)):
    
    s3 = AwsStorage()
    
    tx = ensure_tx(conn) 
    try:
        mProspect = PropectModel(conn)
        mProspectDocument  = ProspectDocumentModel(conn)
        
        documents = {}
        
        for field, up in payload.iter_files():
            
            size = await size_guard(up, calculate_max_bytes(5))
            key = f"documents/{id}/{field}/{uuid4()}.{get_full_extension(up.filename or field)}"
            
            upload = s3.upload_file('documentos-prospectos', key, up.file)
            if not upload:
                return ResponseHelper(
                    code=400,
                    message="Request failed",
                    errors=['error_upload_storage'],
                )
                
            documents[fields[field]] = key
    
        
        documents['prospecto_id'] = id
        documents['csd_clave'] = payload.csd_password
        documents['rfc'] = payload.taxid
        documents['regimen'] = payload.regimen
        documents['creacion'] = now()
        
        
        documents_id = await mProspectDocument.update(
            "prospecto_id = '{prospecto_id}'".format(prospecto_id=id),
            documents
        )
        if not documents_id:
            rollback_tx(conn, tx)
            return ResponseHelper(
                code=400,
                message="Request failed",
                errors=['error_update_prospect_document'],
            )
    
        commit_tx(conn, tx)
        return ResponseHelper(
            code=200,
            message="Request completed successfully",
            data={
                'prospect_id': id
            }
        )

    except Exception as e:
        rollback_tx(conn, tx)
        return ResponseHelper(
            code=400,
            message="Request failed",
            errors=[str(e) or "exception_controller"],
        )

    
