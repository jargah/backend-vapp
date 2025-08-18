from database.MySQLModel import MySQLModel

class PassengersOTPModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.otp_pasajero'
        super().__init__(db, table)
      