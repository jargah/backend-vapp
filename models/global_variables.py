from database.MySQLModel import MySQLModel

class GlobalVariablesModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.control_panel'
        super().__init__(db, table)
      