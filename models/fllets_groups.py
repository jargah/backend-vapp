from database.MySQLModel import MySQLModel

class FleetsGroupsModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.fleets_groups'
        super().__init__(db, table)
      