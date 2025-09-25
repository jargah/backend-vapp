from database.MySQLModel import MySQLModel

class OperatorsModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.operador'
        super().__init__(db, table)
        self.datatable_col_names = [
            'id',
            'username',
            'fullname',
            'phone',
            'taxid',
            'curp',
            'sex',
            'birthday',
            'email',
            'travels',
            'score',
            'balance'
        ]
        
    async def list(self, database: bool = True, page: int = 2, rows: int = 20, search: str = "", order_by: str = "id", order_asc: bool = False):
        
        try:
            SQL = """
                SELECT 
                    o.id_operador AS id,
                    o.usuario AS username,
                    CONCAT(o.nombre, ' ', o.ap_paterno, ' ', o.ap_materno) AS fullname,
                    o.telefono AS phone,
                    o.rfc_operador AS taxid,
                    o.curp,
                    o.sexo AS sex,
                    o.fecha_nacimiento AS birthday,
                    o.email,
                    o.viajes_realizados AS travels,
                    o.calificacion AS score,
                    o.saldo AS balance
                FROM ven_app_api.operador o
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
      