from database.MySQLModel import MySQLModel

class TaxiRequestQueueModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.taxi_solicitud_servicio_cola'
        super().__init__(db, table)
      