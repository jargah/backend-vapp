from database.MySQLModel import MySQLModel

class RegimenModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.regimen_fiscal'
        super().__init__(db, table)
      