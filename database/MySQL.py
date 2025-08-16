from typing import Any
import logging
from sqlalchemy import create_engine, text
from configuration.config import configuration

class MySQL:
    def __init__(self) -> Any:
        self.host = configuration['host']
        self.user = configuration['user']
        self.password = configuration['password']
        self.database = configuration['database']
        self.port = configuration['port']
        self.db = None


    async def connect(self):
        engine = create_engine(
            f'mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
            
        )

        try:
            logging.info('database_connection_success')
            self.db = engine.connect()
            return self.db
        except Exception as e:
            logging.error('database_connection_error', {
                'detail': str(e)
            })
            return None
        
    async def beginTransaction(self):
        return await self.db.begin()
    
    async def commit(self):
        return await self.db.commit()
    
    async def rollback(self):
        return await self.db.rollback()
    
    async def query(self, sql: str):
        try:
            result = self.db.execute(text(sql))

            print(f'db query => {result}')

            return result
        except Exception as err:
            print(err)
            logging.error('database_query_error', {
                'detail': str(err)
            })
            return None
            
    async def update(self, table: str, data: dict, where: str):
        sql = f'UPDATE {table} SET'

        for f in data:
            if data[f] != None:
                if type(data[f]) is bool:
                    data[f] = data[f] if '1' else '0'
                sql += f' {f} = "{data[f]}",'
            else:
                sql += f' {f} = "{data[f]}",'
        
        sql = f'{sql[:-1]} WHERE ${where}'

        logging.debug(sql)

        return await self.query(sql)
    
    async def insert(self, table: str, data: dict):
        sql = f'INSERT TO {table} ('
        values = 'VALUES ('

        for field in data:
            if data[field] != None:
                if type(data[field]) is bool:
                    data[field] = data[field] if '1' else '0'
               
                sql += f'{field},'
                sql += type(data[field]) is int if f'{data[field]},' else f'"{data[field]}",'
            else:
                sql += f'{field},'

        
        sql = sql[:-1]
        values = values[:-1]

        sql += f') {values})'

        logging.debug(sql)

        return await self.query(sql)
    
    def end(self):
        self.db.close()