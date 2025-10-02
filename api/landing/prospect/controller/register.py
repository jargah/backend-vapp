from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.engine import Connection

from database.MySQL import get_db, ensure_tx, commit_tx, rollback_tx
from api.landing.prospect.dto.register import RegisterDTO
from models.prospect import PropectModel
from models.prospect_vehicle import ProspectVehicleModel
from helpers.response import ResponseHelper
from utils.globals import split_fullname
from utils.datetime import now
from uuid import uuid4

register = APIRouter()

@register.post(
    "/register", 
    response_model=dict,
    name=""
)
async def controller(dto: RegisterDTO, conn: Connection = Depends(get_db)):
    
    tx = ensure_tx(conn) 
    
    uid = uuid4()
    
    try:
        mProspect = PropectModel(conn)
        vehicle_model  = ProspectVehicleModel(conn)

        created_at = now()

        id_prospect = await mProspect.insert({
            "uid": str(uid),
            "nombre": dto.first_name,
            "apellido_paterno": dto.last_name,
            "apellido_materno": dto.second_surname,
            "email": dto.email,
            "telefono": dto.phone,
            "flotilla": dto.is_fleet,
            "conductor": dto.is_operator,
            "estatus": "pendiente",
            "activo": True,
            "creacion": created_at,
        })
        
        
        if not id_prospect:
            return ResponseHelper(
                code=400,
                message="Request failed",
                errors=['error_prospect_no_create'],
            )


        for v in dto.vehicles or []:
            id_propect_vehicule = await vehicle_model.insert({
                "id_prospecto": id_prospect,
                "id_vehiculo": v.branch,
                "model": v.branch,
                "anio": v.year,
                "placa": v.number_plate,
                "activo": True,
                "creacion": created_at,
            })
            
            if not id_propect_vehicule:
                return ResponseHelper(
                    code=400,
                    message="Request failed",
                    errors=['error_prospect_vehicle_no_create'],
                )
                
        commit_tx(conn, tx)
        return ResponseHelper(
            code=200,
            message="Request completed successfully",
            data={
                'uid': uid
            },
        )

    except Exception as e:
        rollback_tx(conn, tx)
        return ResponseHelper(
            code=400,
            message="Request failed",
            errors=[str(e) or "exception_controller"],
        )

    
