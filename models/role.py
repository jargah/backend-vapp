from database.MySQLModel import MySQLModel

class RoleModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.role'
        super().__init__(db, table)
      