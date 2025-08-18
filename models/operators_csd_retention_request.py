from database.MySQLModel import MySQLModel

class OperatorsCSDRetentionRequestModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.operador_csd_retencion_servicio'
        super().__init__(db, table)
      