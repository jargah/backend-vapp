from database.MySQLModel import MySQLModel

class ServiceModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.servicio'
        super().__init__(db, table)
        self.datatable_col_names = [
            'id',
            'name',
        ]
        
    async def list(self, database: bool = True, page: int = 2, rows: int = 20, search: str = "", order_by: str = "id", order_asc: bool = False):
        
        try:
            SQL = """
                SELECT 
                    s.id_servicio AS id,
                    s.direccion_ori AS origin,
                    s.direccion_dst AS destination,
                    s.lat_ori AS latitud_origin,
                    s.lon_ori AS longitud_origin,
                    s.lat_dst AS latitud_destination,
                    s.lon_dst AS longitud_destination,
                    s.distancia AS distance,
                    s.tiempo AS time,
                    s.costo AS amount,
                    s.hora_llegada_origen AS departure_origin,
                    s.hora_llegada_destino AS arrival_destination
                FROM ven_app_api.servicio s
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
                SELECT 
                    s.id_servicio AS id,
                    s.direccion_ori AS origin,
                    s.direccion_dst AS destination,
                    s.lat_ori AS latitud_origin,
                    s.lon_ori AS longitud_origin,
                    s.lat_dst AS latitud_destination,
                    s.lon_dst AS longitud_destination,
                    s.distancia AS distance,
                    s.tiempo AS time,
                    s.costo AS amount,
                    s.costo_final AS amount_final,
                    s.pctj_comision AS tax,
                    s.hora_llegada_origen AS departure_origin,
                    s.hora_llegada_destino AS arrival_destination
                FROM ven_app_api.servicio s
                WHERE s.id_servicio = '{id}'
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
                    s.id_servicio AS id,
                    s.direccion_ori AS origin,
                    s.id_taxi AS id_taxi,
                    s.id_pasajero AS id_pasajero,
                    s.direccion_dst AS destination,
                    s.lat_ori AS latitud_origin,
                    s.lon_ori AS longitud_origin,
                    s.lat_dst AS latitud_destination,
                    s.lon_dst AS longitud_destination,
                    s.distancia AS distance,
                    s.tiempo AS time,
                    s.costo AS amount,
                    s.costo_final AS amount_final,
                    s.pctj_comision AS tax,
                    s.hora_llegada_origen AS departure_origin,
                    s.hora_llegada_destino AS arrival_destination
                FROM ven_app_api.servicio s
                WHERE s.id_servicio = '{id}'
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
      