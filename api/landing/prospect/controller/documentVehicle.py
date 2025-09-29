from __future__ import annotations

from fastapi import APIRouter, Depends
from helpers.AWSS3 import AwsStorage
from sqlalchemy.engine import Connection
from uuid import uuid4

from database.MySQL import get_db, ensure_tx, commit_tx, rollback_tx
from api.landing.prospect.dto.documentVehicle import DocumentVehicleDTO
from models.prospect import PropectModel
from models.prospect_document import ProspectDocumentModel
from helpers.response import ResponseHelper
from utils.globals import calculate_max_bytes, get_full_extension, safe_filename, size_guard, split_fullname
from utils.datetime import now

fields = {
    'circulation_card': 'tarjeta_circulacion',
    'insurance_policy': 'poliza_seguro',
    'invoice': 'factura',
    'verification_sticker': 'calcomania_verificacion'
}

vehicle = APIRouter()

@vehicle.post(
    "/{id}/document-vehicle", 
    response_model=dict,
    name=""
)
async def controller(id: int, payload: DocumentVehicleDTO = Depends(DocumentVehicleDTO.as_form), conn: Connection = Depends(get_db)):
    
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
        documents['creacion'] = now()
        
        documents_id = await mProspectDocument.insert(documents)
        if not documents_id:
            rollback_tx(conn, tx)
            return ResponseHelper(
                code=400,
                message="Request failed",
                errors=['error_create_prospect_document'],
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

    
