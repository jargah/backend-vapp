from database.MySQLModel import MySQLModel

class VehicleModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.vehiculo'
        super().__init__(db, table)
        self.datatable_col_names = [
            'id_vehiculo',
            'nombre',
            'marca',
            'modelo',
            'activo',
        ]
        
    async def list(self, database: bool = True, page: int = 2, rows: int = 20, search: str = "", order_by: str = "id", order_asc: bool = False):
        
        try:
            SQL = """
                SELECT 
                    * 
                FROM ven_app_api.vehiculos
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
        
        
    async def findById(self, id_vehiculo: int):
        
        try:
            SQL = """
                SELECT * FROM ven_app_api.vehiculos WHERE id_vehiculo = '{id_vehiculo}'
            """.format(id_vehiculo=id_vehiculo)
            
            
            result = await self.query(
                sql=SQL,
                fetch='one',
                debug=True
            )
            
            return result
        except Exception as e:
            print(e)
            return None
      