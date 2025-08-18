from database.MySQLModel import MySQLModel

class FleetsModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.fleets'
        super().__init__(db, table)
      