from database.MySQLModel import MySQLModel

class RolesModel(MySQLModel):
    
    def __init__(self, db) -> any:
        table = 'administrator.role'
        super().__init__(db, table)
        self.datatable_col_names = ['id_role', 'name', 'active', 'creation']
        
        
    async def list(self, database: bool = True, page: int = 2, rows: int = 20, search: str = "", order_by: str = "id", order_asc: bool = False):
        
        try:
            SQL = """
                SELECT 
                    r.id_role AS id,
                    r.name,
                    r.description,
                    r.active,
                    r.creation
                FROM administrator.role r
            """
            
            result = await self.datatable(
                base_sql=SQL,
                database=database,
                page=page,
                rows=rows,
                search=search,
                order_by=order_by,
                order_asc=order_asc,
                search_columns=[]
            )
            
            return result
        except Exception as e:
            return None
        
        
        