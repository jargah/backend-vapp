from database.MySQLModel import MySQLModel

class PassengersModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.pasajero'
        super().__init__(db, table)
      