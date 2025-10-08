from database.MySQLModel import MySQLModel

class RouteServiceModel(MySQLModel):
    
    def __init__(self, db) -> any:
        table = 'ven_app_api.ruta_servicio'
        super().__init__(db, table)
        self.datatable_col_names = []
        
    async def findByService(self, id_service: int):
        
        try:
            SQL = """
                SELECT 
                    rs.id_ruta_servicio AS route_service_id,
                    rs.id_servicio AS service_id,
                    rs.latitud AS latitude,
                    rs.longitud AS longitude,
                    cc.nombre_causa_cancelacion AS movement,
                    rs.fecha AS creation
                FROM ven_app_api.ruta_servicio  rs
                    LEFT JOIN ven_app_api.causa_cancelacion cc ON cc.id_causa_cancelacion = rs.id_causa_cancelacion
                WHERE rs.id_servicio = '{id_service}' 
                    AND rs.longitud <> 0
                    AND rs.longitud <> 0
                ORDER BY rs.id_ruta_servicio ASC
            """.format(id_service=id_service)
            
            result = await self.query(
                sql=SQL,
                fetch='all',
                debug=True
            )
            
            return result
        except Exception as e:
            print(e)
            return None
    
    async def findById(self, id_route_service: int):
        
        try:
            SQL = """
                SELECT 
                    rs.id_ruta_servicio AS route_service_id,
                    rs.id_servicio AS service_id,
                    rs.latitud AS latitude,
                    rs.longitud AS longitude,
                    cc.nombre_causa_cancelacion AS movement,
                    rs.fecha AS creation
                FROM ven_app_api.ruta_servicio  rs
                    LEFT JOIN ven_app_api.causa_cancelacion cc ON cc.id_causa_cancelacion = rs.id_causa_cancelacion
                WHERE rs.id_ruta_servicio = '{id_route_service}'
                    AND rs.longitud <> 0
                    AND rs.longitud <> 0 
                ORDER BY rs.id_ruta_servicio ASC
            """.format(id_route_service=id_route_service)
            
            
            result = await self.query(
                sql=SQL,
                fetch='one',
                debug=True
            )
            
            return result
        except Exception as e:
            print(e)
            return None
    
        
        
        