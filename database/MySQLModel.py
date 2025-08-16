from database.MySQL import MySQL

class MySQLModel:
    def __init__(self, db: MySQL, table: str):
        self.db = db
        self.table = table
        # self.datatable_col_names = ''

    def getTableName(self):
        return self.table
    
    def getColNames(self):
        return self.datatable_col_names
    
    def insert(self, data: dict):
        return self.db.insert(table=self.table, data=data)
    
    def update(self, data:dict, where: str):
        return self.update(data=data, where=where)
    
    def featchAllRows(self):
        sql = f'SELECT * FROM {self.table}'
        return self.db.query(sql)
    
    async def selectAll(self, where='', order = 'ASC', fields =  None):
        internal_fields = ''
        if fields == None:
            internal_fields = '*'
        else:
            internal_fields = fields

        sql = f'SELECT {internal_fields} FROM {self.table}'

        if where != '':
            sql += f' WHERE {where}'

        if order == 'ASC':
            sql += f' ORDER BY 1 ASC'
        elif order == 'DESC':
            sql += f' ORDER BY 1 DESC'

        result = await self.db.query(sql)
        if not result:
            return None
        
        data = []
        for key in result.fetchall():
            data.append(key._key_to_index)
        
        return data
    
    async def selectFirst(self, where='', order = 'ASC', fields = None):
        internal_fields = ''
        if fields == None:
            internal_fields = '*'
        else:
            internal_fields = fields

        sql = f'SELECT {internal_fields} FROM {self.table}'

        if where != '':
            sql += f' WHERE {where}'

        if order == 'ASC':
            sql += f' ORDER BY 1 ASC'
        elif order == 'DESC':
            sql += f' ORDER BY 1 DESC'

        result = await self.db.query(sql)
        if not result:
            return None
        
        return result.fetchone()._key_to_index
