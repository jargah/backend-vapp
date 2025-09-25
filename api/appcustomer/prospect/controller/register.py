from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.engine import Connection

from database.MySQL import get_db, ensure_tx, commit_tx, rollback_tx
from api.landing.prospect.dto.prospect import ProspectDTO
from models.prospect import PropectModel
from models.prospect_vehicle import ProspectVehicleModel
from helpers.response import ResponseHelper
from utils.globals import split_fullname
from utils.datetime import now

register = APIRouter()

@register.post(
    "/register", 
    response_model=dict,
    name=""
)
async def controller(dto: ProspectDTO, conn: Connection = Depends(get_db)):
    
    tx = ensure_tx(conn) 
    try:
        mProspect = PropectModel(conn)
        vehicle_model  = ProspectVehicleModel(conn)

        names = split_fullname(dto.fullname)
        created_at = now()

        id_prospect = await mProspect.insert({
            "nombre": names.get("first_name"),
            "apellido_paterno": names.get("last_name"),
            "apellido_materno": names.get("second_surname"),
            "email": dto.email,
            "telefono": dto.phone,
            "propietario_vehiculo": dto.property_vehicle,
            "propietario_vehiculo_secundario": dto.property_vehicle_second,
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
                "id_vehiculo": v.id_vehicles,
                "marca": v.branch,
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
            data="OK",
        )

    except Exception as e:
        rollback_tx(conn, tx)
        return ResponseHelper(
            code=400,
            message="Request failed",
            errors=[str(e) or "exception_controller"],
        )

    
