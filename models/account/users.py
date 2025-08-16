from database.MySQLModel import MySQLModel

class UserModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'macaco.users'
        super().__init__(db, table)
      