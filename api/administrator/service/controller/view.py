from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union, List
from database.MySQL import get_db
from api.administrator.auth.dto.login import LoginDTO
from starlette.requests import Request
from models.service import ServiceModel
from models.taxi import TaxiModel
from models.passengers import PassengersModel
from models.route_service import RouteServiceModel
from helpers.response import ResponseHelper
from schemas.datatable import DataTableQueryDTO, datatable_query_dependency
from datetime import datetime, timedelta




view = APIRouter()
@view.get("/{id}/view", 
    response_model=dict, 
    name='',
)
async def controller(id: int, db: Session = Depends(get_db)):
    try:
        
        if not id:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_empty_id']
            )

        mServiceModel = ServiceModel(db)
        mTaxiModel = TaxiModel(db)
        mPassengersModel = PassengersModel(db)
        mRouteServiceModel = RouteServiceModel(db)
        
        service = await mServiceModel.view(id=id) 
        
        if service == None:
            return ResponseHelper(
                code=400,
                message='Request Failed',
                errors=['error_service_no_found']
            )
            
        taxi = await mTaxiModel.findById(id_taxi=service['id_taxi'])
        passenger = await mPassengersModel.view(id=service['id_pasajero'])
        route_service = await mRouteServiceModel.findByService(id_service=service['id'])
        
        
        dist_m = float(service.get('distance') or 0.0)
        time_s = int(service.get('time') or 0)
        amount = float(service.get('amount') or 0.0)
        amount_final = float(service.get('amount_final') or 0.0)
        tax_rate = float(service.get('tax') or 0.0)  # interpreto como tasa (e.g., 0.2 = 20%)

        # Derivados básicos
        distance_km = dist_m / 1000.0
        duration_min = time_s / 60.0
        duration_hhmmss = str(timedelta(seconds=time_s))  # '1:27:35'
        avg_speed_kmh = (distance_km / (time_s / 3600.0)) if time_s > 0 else 0.0

        # Unitarios
        price_per_km = (amount / distance_km) if distance_km > 0 else 0.0
        price_final_per_km = (amount_final / distance_km) if distance_km > 0 else 0.0

        # Impuestos (dos interpretaciones comunes)
        # 1) Exclusivo: amount es subtotal sin impuestos
        tax_amount_exclusive = amount * tax_rate
        total_if_exclusive = amount + tax_amount_exclusive

        # 2) Incluido: amount ya trae impuestos
        tax_amount_included = amount * (tax_rate / (1.0 + tax_rate)) if (1.0 + tax_rate) != 0 else 0.0
        subtotal_if_inclusive = amount - tax_amount_included

        # Consistencia timestamps vs 'time'
        ts_dep = service.get('departure_origin')
        ts_arr = service.get('arrival_destination')
        diff_seconds = None
        if ts_dep and ts_arr:
            try:
                dep_dt = datetime.fromisoformat(ts_dep)
                arr_dt = datetime.fromisoformat(ts_arr)
                diff_seconds = int((arr_dt - dep_dt).total_seconds())
            except Exception:
                diff_seconds = None

        metrics = {
            "distance_m": dist_m,
            "distance_km": round(distance_km, 6),
            "duration_s": time_s,
            "duration_min": round(duration_min, 6),
            "duration_hhmmss": duration_hhmmss,  # e.g. "01:27:35"
            "avg_speed_kmh": round(avg_speed_kmh, 6),

            "unit_prices": {
                "per_km_from_amount": round(price_per_km, 6),
                "per_km_from_amount_final": round(price_final_per_km, 6),
            },

            "tax_rate_assumed": tax_rate,
            "tax_calc_assuming_exclusive": {
                "tax_amount": round(tax_amount_exclusive, 6),
                "total": round(total_if_exclusive, 6),
                "note": "Se asume amount SIN impuestos.",
            },
            "tax_calc_assuming_inclusive": {
                "tax_amount": round(tax_amount_included, 6),
                "subtotal": round(subtotal_if_inclusive, 6),
                "note": "Se asume amount CON impuestos.",
            },

            "timestamps_check": {
                "departure_origin": ts_dep,
                "arrival_destination": ts_arr,
                "diff_seconds": diff_seconds,
                "consistency_note": (
                    "Inconsistencia: 'time' = {} s, pero timestamps = {} s."
                    .format(time_s, diff_seconds) if (diff_seconds is not None and diff_seconds != time_s) else "OK"
                ),
            },
        }

        data = {
            "service": service,
            "metrics": metrics,
            "passenger": passenger,
            "taxi": taxi,
            "route": route_service
        }
            
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