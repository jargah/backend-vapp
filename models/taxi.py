from database.MySQLModel import MySQLModel

class TaxiModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.taxi'
        super().__init__(db, table)
      