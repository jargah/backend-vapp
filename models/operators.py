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
      
      
    async def view(self, id: int):
        
        try:
            SQL = """
                SELECT 
                    o.id_operador AS id,
                    o.nombre AS first_name,
                    o.ap_paterno AS last_name,
                    o.ap_materno AS second_surname,
                    o.telefono AS phone,
                    oe.id_empresa AS empresa_operador_id,
                    oe.nombre_razon_social AS empresa_operador,
                    o.foto AS picture,
                    o.rfc_operador AS taxid,
                    o.curp AS curp,
                    o.sexo AS gender,
                    o.fecha_nacimiento AS birthday,
                    o.usuario AS username,
                    o.calle_num AS address,
                    o.colonia AS suburb,
                    o.codigo_postal_operador AS zipcode,
                    o.estado AS state,
                    o.municipio AS municipality,
                    o.email,
                    o.email_verificado AS email_verify,
                    o.saldo AS balance,
                    o.calificacion AS score,
                    o.viajes_realizados AS travels,
                    o.saldo_pendiente AS balance_pending,
                    o.fecha_registro AS register_date,
                    o.saldo_facturar_venapp AS balance_invoice,
                    o.activo AS active,
                    t.marca AS branch,
                    t.modelo AS model,
                    t.num_eco AS number_eco,
                    t.placas AS number_plate,
                    t.serie AS serie,
                    t.submarca AS sub_branch,
                    te.id_empresa AS taxi_empresa_id,
                    te.nombre_razon_social AS taxi_empresa,
                    tt.id_tipo_taxi AS type_taxi_id,
                    tt.nombre_tipo_taxi AS type_taxi,
                    tm.id_tipo_motor AS type_motor_id,
                    tm.nombre_tipo_motor AS type_motor
                FROM ven_app_api.operador o
                    LEFT JOIN ven_app_api.empresa oe ON oe.id_empresa = o.id_empresa 
                    LEFT JOIN ven_app_api.taxi t ON t.id_taxi = o.id_taxi
                    LEFT JOIN ven_app_api.tipo_taxi tt ON tt.id_tipo_taxi = t.id_tipo_taxi
                    LEFT JOIN ven_app_api.tipo_motor tm ON tm.id_tipo_motor = t.id_tipo_motor
                    LEFT JOIN ven_app_api.empresa te ON te.id_empresa = t.id_empresa
                WHERE o.id_operador = '{id}'
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