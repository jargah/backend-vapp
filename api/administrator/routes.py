from fastapi import APIRouter, Depends
from  interceptors.token import Token
from interceptors.credentials import Credentials

from api.administrator.auth.routes import auth
from api.administrator.fleets.routes import fleets
from api.administrator.configurations.routes import configurations

# Operators
from api.administrator.operators.routes import operators
from api.administrator.operators_taxid.routes import operators as operatorsTaxId
from api.administrator.operators_invoice.routes import operators as operatorsInovice

# Passengers
from api.administrator.passengers.routes import passengers
from api.administrator.passengers_taxid.routes import passengers as passengersTaxId

# taxi
from api.administrator.taxi.routes import taxi
from api.administrator.taxi_request_history.routes import taxi as taxiRequestHistory

# Referral
from api.administrator.referral.routes import referral
from api.administrator.referral_benefits.routes import referral as referralBenefit
from api.administrator.referral_movements.routes import referral as referralMovements
from api.administrator.referral_operators.routes import referral as referralOperators
from api.administrator.referral_program.routes import referral as referralProgram
from api.administrator.referral_redemptions.routes import referral as referralRedemtions

administrator = APIRouter(
    prefix='/administrator'
)

administrator.include_router(auth)
administrator.include_router(fleets)
administrator.include_router(configurations)

# OPERATORS
administrator.include_router(operators)
administrator.include_router(operatorsTaxId)
administrator.include_router(operatorsInovice)

# PASSENGERS
administrator.include_router(passengers)
administrator.include_router(passengersTaxId)

# REFERRAL
administrator.include_router(referral)
administrator.include_router(referralBenefit)
administrator.include_router(referralMovements)
administrator.include_router(referralOperators)
administrator.include_router(referralProgram)
administrator.include_router(referralRedemtions)


#TAXI
administrator.include_router(taxi)
administrator.include_router(taxiRequestHistory)
