from database.MySQLModel import MySQLModel

class UsersModel(MySQLModel):
    
    def __init__(self, db) -> any:
        table = 'administrator.users'
        super().__init__(db, table)
        self.datatable_col_names = ['id_user', 'first_name', 'last_name', 'username', 'email', 'phone']
        
        
    async def list(self, database: bool = True, page: int = 2, rows: int = 20, search: str = "", order_by: str = "id", order_asc: bool = False):
        
        try:
            SQL = """
                SELECT 
                    u.id_user AS id,
                    u.first_name,
                    u.last_name,
                    u.username,
                    u.email,
                    u.phone
                FROM administrator.users u
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
        
        
        