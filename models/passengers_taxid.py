from database.MySQLModel import MySQLModel

class PassengersTaxId(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.pasajero_datos_fiscales'
        super().__init__(db, table)
      