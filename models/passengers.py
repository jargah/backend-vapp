from database.MySQLModel import MySQLModel

class PassengersModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.pasajero'
        super().__init__(db, table)
        self.datatable_col_names = [
            'id',
            'fullname',
            'phone',
            'email',
            'gender',
            'active',
            'register_date'
            
        ]
      
    async def list(self, database: bool = True, page: int = 2, rows: int = 20, search: str = "", order_by: str = "id", order_asc: bool = False):
        
        try:
            SQL = """
                SELECT 
                    p.id_pasajero AS id,
                    CONCAT(p.nombre, ' ', p.ap_paterno, ' ', p.ap_materno) AS fullname,
                    p.telefono AS phone,
                    p.email,
                    p.genero AS gender,
                    p.activo AS active,
                    p.fecha_registro AS register_date
                FROM ven_app_api.pasajero p
                WHERE p.activo = '1'
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
                    p.id_pasajero AS id,
                    p.nombre AS first_name,
                    p.ap_paterno AS last_name,
                    p.ap_materno AS second_surname,
                    p.telefono AS phone,
                    p.cp AS zipcode_passenger,
                    p.genero AS gender,
                    p.email,
                    p.usuario AS username,
                    p.fecha_registro AS register_date,
                    p.calificacion AS score,
                    p.verificacion_facial AS facial_verification,
                    pdf.codigo_postal AS zipcode_fiscal,
                    pdf.nombre_razon_social AS tax,
                    pdf.rfc AS taxid
                FROM ven_app_api.pasajero p
                    LEFT JOIN ven_app_api.pasajero_datos_fiscales AS pdf ON pdf.id_pasajero = p.id_pasajero
                WHERE p.id_pasajero = '{id}'
                    AND p.activo  = '1'
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