from database.MySQLModel import MySQLModel

class OperatorsInvoiceModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.operador_factura'
        super().__init__(db, table)
      