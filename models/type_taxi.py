from database.MySQLModel import MySQLModel

class TypeTaxi(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.tipo_taxi'
        super().__init__(db, table)
        self.datatable_col_names = [
            'id',
            'name',
        ]
        
    async def list(self, database: bool = True, page: int = 2, rows: int = 20, search: str = "", order_by: str = "id", order_asc: bool = False):
        
        try:
            SQL = """
                SELECT 
                    tm.id_tipo_taxi AS id,
                    tm.nombre_tipo_taxi AS name
                FROM ven_app_api.tipo_taxi tm
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
        
        
    async def findById(self, id: int):
        
        try:
            SQL = """
                SELECT * FROM ven_app_api.tipo_taxi WHERE id_tipo_taxi = '{id}'
            """.format(id=id)
            
            
            result = await self.query(
                sql=SQL,
                fetch='one',
                debug=True
            )
            
            return result
        except Exception as e:
            print(e)
            return None
        
    async def view(self, id: int):
        
        try:
            SQL = """
                SELECT 
                    tm.id_tipo_taxi AS id,
                    tm.nombre_tipo_taxi AS name
                FROM ven_app_api.tipo_taxi tm
                WHERE tm.id_tipo_taxi = '{id}'
            """.format(id=id)
            
            
            result = await self.query(
                sql=SQL,
                fetch='one',
                debug=True
            )
            
            return result
        except Exception as e:
            print(e)
            return None
      