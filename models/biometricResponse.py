from database.MySQLModel import MySQLModel

class BiometricResponseModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'biometric.response'
        super().__init__(db, table)
      