from sqlalchemy import text
class MySQLModel:
    def __init__(self, db, table: str):
        self.db = db
        self.table = table
        # self.datatable_col_names = ''

    def getTableName(self):
        return self.table
    
    def getColNames(self):
        return self.datatable_col_names
    
    async def insert(self, data: dict):
        
        columns = ', '.join(data.keys())
        
        values = ''
        for value in data.values():
            if isinstance(value, str) and value.find('TO_DATE') != -1:
                values += f"{value}, "
            elif isinstance(value, str) and value.find('TO_TIMESTAMP') != -1:
                values += f"{value}, "
            elif isinstance(value, str):
                values += f"'{value}', "
            else:
                values += f"{value}, "
        
        values = values[:-2]
        sql = f"INSERT INTO {self.table} ({columns}) VALUES ({values})"
        
        print(sql)

        result = self.db.execute(text(sql))
        self.db.commit()
        return result.lastrowid
    
    async def update(self, where: str, data: dict):
        set_values = ""
        for column, value in data.items():
            if isinstance(value, str) and value.find('TO_DATE') != -1:
                set_values += f"{column} = {value}, "
            elif isinstance(value, str) and value.find('TO_TIMESTAMP') != -1:
                set_values += f"{column} = {value}, "
            elif isinstance(value, str):
                set_values += f"{column} = '{value}', "
            else:
                set_values += f"{column} = {value}, "

        set_values = set_values[:-2]  # quitar última coma

        sql = f"UPDATE {self.table} SET {set_values} WHERE {where}"

        print(sql)  # debug

        result = self.db.execute(text(sql))
        self.db.commit()
        return result.rowcount
    
    
    async def featchAllRows(self):
        sql = f'SELECT * FROM {self.table}'
        return await self.db.query(sql)
    
    async def selectAll(self, where='', order = 'ASC', fields =  None):
        try:
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

            query = text(sql)
            result = self.db.execute(query)
            result = result.mappings().all()
            if result is None:
                return None
            
            data = list()
            for key in result:
                data.append(key)
            
            return data
        except (ValueError, TypeError) as e:
            print(e)
            return None
    
    async def selectFirst(self, where='', order = 'ASC', fields = None):
        try:
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
            
            query = text(sql)
            
            print(query)
            
            
            result = self.db.execute(query)
            result = result.mappings().fetchone()
            
            if result is None:
                print(22)
                return None
            
            print(result)
            
            return result
        except (ValueError, TypeError) as e:
            print('error')
            print(e)
            return None