from database.MySQLModel import MySQLModel

class ApiModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'administrator.api'
        super().__init__(db, table)
      