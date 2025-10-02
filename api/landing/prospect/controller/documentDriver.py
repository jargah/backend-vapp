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
    "/{uid}/document-fiscal", 
    response_model=dict,
    name=""
)
async def controller(uid: str, payload: DocumentDriverDTO = Depends(DocumentDriverDTO.as_form), conn: Connection = Depends(get_db)):
    
    s3 = AwsStorage()
    
    tx = ensure_tx(conn) 
    try:
        mProspect = PropectModel(conn)
        mProspectDocument  = ProspectDocumentModel(conn)
        
        prospect = await mProspect.selectFirst("uid = '{uid}'".format(uid=uid))
        if not prospect:
            rollback_tx(conn, tx)
            return ResponseHelper(
                code=400,
                message="Request failed",
                errors=['error_propect_no_found'],
            )
        
        documents = {}
        
        for field, up in payload.iter_files():
            
            size = await size_guard(up, calculate_max_bytes(5))
            key = f"documents/{uid}/{field}.{get_full_extension(up.filename or field)}"
            
            upload = s3.upload_file('documentos-prospectos', key, up.file)
            if not upload:
                return ResponseHelper(
                    code=400,
                    message="Request failed",
                    errors=['error_upload_storage'],
                )
                
            documents[fields[field]] = key
    
        
        documents['csd_clave'] = str(payload.csd_password)
        documents['rfc'] = payload.taxid
        documents['regimen'] = payload.regimen
        documents['creacion'] = now()
        
        
        documents_id = await mProspectDocument.update(
            "prospecto_id = '{id}'".format(id=prospect['id_prospecto']),
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
                'documents': True
            }
        )

    except Exception as e:
        rollback_tx(conn, tx)
        return ResponseHelper(
            code=400,
            message="Request failed",
            errors=[str(e) or "exception_controller"],
        )

    
