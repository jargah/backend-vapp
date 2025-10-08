from fastapi import APIRouter, Depends
from interceptors.credentials import Credentials

from api.administrator.auth.routes import auth
from api.administrator.profile.routes import profile

# Configuration
from api.administrator.users.routes import users
from api.administrator.roles.routes import roles

# Prospects 
from api.administrator.prospects.routes import prospects


# OPERATION
from api.administrator.operators.routes import operators
from api.administrator.passengers.routes import passengers
from api.administrator.service.routes import service

# taxi
from api.administrator.taxi.routes import taxi

# CATALOGS
from api.administrator.vehicles.routes import vehicles
from api.administrator.type_motor.routes import typeMotor
from api.administrator.type_payment.routes import typePayment
from api.administrator.type_taxi.routes import typeTaxi


administrator = APIRouter(
    prefix='/administrator'
)

administrator.include_router(auth)
administrator.include_router(profile)

# Configuration
administrator.include_router(users)
administrator.include_router(roles)

# PROSPECTS
administrator.include_router(prospects)

# OPERATION
administrator.include_router(operators)
administrator.include_router(passengers)
administrator.include_router(service)

#TAXI
administrator.include_router(taxi)

# CATALOGS
administrator.include_router(vehicles)
administrator.include_router(typeMotor)
administrator.include_router(typePayment)
administrator.include_router(typeTaxi)

