from database.MySQLModel import MySQLModel

class OperatorsTaxIdModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.operador_datos_fiscales'
        super().__init__(db, table)
      