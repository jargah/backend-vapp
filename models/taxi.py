from database.MySQLModel import MySQLModel

class TaxiModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.taxi'
        super().__init__(db, table)
        self.datatable_col_names = [
            'id',
            'placa',
            'model',
            'color',
            'type_taxi',
            'marca',
            'submarca',
            'motor',
            'empresa'
        ]
        
    async def list(self, database: bool = True, page: int = 2, rows: int = 20, search: str = "", order_by: str = "id", order_asc: bool = False):
        
        try:
            SQL = """
                SELECT 
                    t.id_taxi AS id,
                    t.placas AS placa,
                    t.modelo AS model,
                    t.color As color,
                    tt.nombre_tipo_taxi AS type_taxi,
                    t.marca,
                    t.submarca,
                    tm.nombre_tipo_motor AS motor,
                    e.nombre_razon_social AS empresa
                FROM ven_app_api.taxi t
                    INNER JOIN ven_app_api.operador o ON t.id_taxi = o.id_taxi
                    INNER JOIN ven_app_api.tipo_taxi tt ON tt.id_tipo_taxi = t.id_tipo_taxi
                    INNER JOIN ven_app_api.tipo_motor tm ON tm.id_tipo_motor = t.id_tipo_motor
                    INNER JOIN ven_app_api.empresa e ON e.id_empresa = t.id_empresa
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
        
        
    async def findById(self, id_taxi: int):
        
        try:
            SQL = """
                SELECT 
                    t.id_taxi AS id,
                    t.placas AS placa,
                    t.modelo AS model,
                    t.color As color,
                    t.num_eco,
                    t.num_motor,
                    t.serie,
                    tt.id_tipo_taxi,
                    tt.nombre_tipo_taxi AS type_taxi,
                    t.marca,
                    t.submarca,
                    tm.id_tipo_motor,
                    tm.nombre_tipo_motor AS motor,
                    e.id_empresa,
                    e.nombre_razon_social
                FROM ven_app_api.taxi t
                    INNER JOIN ven_app_api.operador o ON t.id_taxi = o.id_taxi
                    INNER JOIN ven_app_api.tipo_taxi tt ON tt.id_tipo_taxi = t.id_tipo_taxi
                    INNER JOIN ven_app_api.tipo_motor tm ON tm.id_tipo_motor = t.id_tipo_motor
                    INNER JOIN ven_app_api.empresa e ON e.id_empresa = t.id_empresa
                WHERE t.id_taxi = '{id_taxi}'
            """.format(id_taxi=id_taxi)
            
            
            result = await self.query(
                sql=SQL,
                fetch='one',
                debug=True
            )
            
            return result
        except Exception as e:
            print(e)
            return None
      