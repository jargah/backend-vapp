from database.MySQLModel import MySQLModel

class OperatorsCSDRetentionModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.operador_csd_retencion'
        super().__init__(db, table)
      