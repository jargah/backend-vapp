from database.MySQLModel import MySQLModel

class TaxiRequestServiceModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.taxi_solicitud_servicio'
        super().__init__(db, table)
      