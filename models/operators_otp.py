from database.MySQLModel import MySQLModel

class OperatorsOTPModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.otp_operador'
        super().__init__(db, table)
      