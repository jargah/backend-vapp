from database.MySQLModel import MySQLModel

class PaymentsModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.pago'
        super().__init__(db, table)
      