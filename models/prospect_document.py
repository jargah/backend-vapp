from database.MySQLModel import MySQLModel

class ProspectDocumentModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.prospecto_documento'
        super().__init__(db, table)
        self.datatable_col_names = [
            
        ]
        
      