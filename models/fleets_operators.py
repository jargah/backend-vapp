from database.MySQLModel import MySQLModel

class FleetOperatorsModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.fleets_operators'
        super().__init__(db, table)
      