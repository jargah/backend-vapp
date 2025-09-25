from database.MySQLModel import MySQLModel

class BiometricLinkModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'biometric.links'
        super().__init__(db, table)
      