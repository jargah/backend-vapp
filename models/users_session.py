from database.MySQLModel import MySQLModel

class UserSessionModel(MySQLModel):
    
    def __init__(self, db) -> any:
        table = 'administrator.users_session'
        super().__init__(db, table)
        self.datatable_col_names = []
        
