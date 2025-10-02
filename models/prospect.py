from database.MySQLModel import MySQLModel

class PropectModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.prospecto'
        super().__init__(db, table)
        self.datatable_col_names = [
            'id',
            'first_name',
            'last_name',
            'second_surname',
            'email',
            'phone',
            'fleet',
            'operator',
            'status',
            'creation'
        ]
        
    async def list(self, database: bool = True, page: int = 2, rows: int = 20, search: str = "", order_by: str = "id", order_asc: bool = False):
        
        try:
            SQL = """
                                
                SELECT
                    *
                FROM (
                    WITH ranked AS (
                        SELECT
                            p.id_prospecto AS id,
                            p.uid,
                            p.nombre AS first_name,
                            p.apellido_paterno AS last_name,
                            p.apellido_materno AS second_surname,
                            p.email,
                            p.telefono AS phone,
                            p.flotilla AS fleet,
                            p.conductor AS operator,
                            p.estatus AS status,
                            p.creacion AS creation,
                            ROW_NUMBER() OVER (PARTITION BY p.email ORDER BY p.creacion DESC) AS rn
                        FROM ven_app_api.prospecto p
                        )
                        SELECT *
                            FROM ranked
                            WHERE rn = 1
                        ORDER BY creation ASC
                ) prospectos
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
      