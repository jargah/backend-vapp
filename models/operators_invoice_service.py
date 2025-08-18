from database.MySQLModel import MySQLModel

class OperatorsInvoiceServiceModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.operador_factura_servicio'
        super().__init__(db, table)
      