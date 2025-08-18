from database.MySQLModel import MySQLModel

class AdministratorModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.administrator'
        super().__init__(db, table)
      