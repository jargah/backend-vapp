from sqlalchemy import text
import re as _re
from typing import List, Optional, Dict, Any, Tuple

class MySQLModel:
    def __init__(self, db, table: str):
        self.db = db
        self.table = table
        self.datatable_col_names = []

    def getTableName(self):
        return self.table
    
    def getColNames(self):
        return self.datatable_col_names
    

    def _split_alias(self, col: str) -> str:
        return col.split(".")[-1] if "." in col else col

    def _safe_identifier_sql(self, name: str | None, allow_dot: bool = True) -> str | None:
        if not name:
            return None
        import re
        pat = r"[A-Za-z0-9_\.]+" if allow_dot else r"[A-Za-z0-9_]+"
        if not re.fullmatch(pat, name):
            return None
        if self.datatable_col_names:
            base = self._split_alias(name)
            return name if base in self.datatable_col_names else None
        return name

    def _build_search_clause_sql(self, search: str | None, search_columns: list[str] | None):
        
        params = {}
        if not search:
            return "", params
        
        cols = search_columns
        if not cols:
            return "", params
        
        import re
        parts = []
        for col in cols:
            if not re.fullmatch(r"[A-Za-z0-9_\.]+", col):
                continue
            parts.append(f"{col} LIKE '%{search}%'")
            
 
        if not parts:
            return "", params
        

        return " (" + " OR ".join(parts) + ") "
    
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
        
    async def datatable(
        self,
        base_sql: str,
        database: bool = True,
        page: int = 1,
        rows: int = 10,
        search: str | None = None,
        order_by: str | None = None,
        order_asc: bool = True,
        search_columns: list[str] | str | None = None,
    ):

        bind = dict({})

        search_columns = self.datatable_col_names

        try:
            page = max(1, int(page))
        except Exception:
            page = 1
        try:
            rows = max(1, int(rows))
        except Exception:
            rows = 10

        order_by = str(order_by) if order_by not in (None, "", False) else None
        search = str(search) if (search not in (None, "") and search is not False) else None

        search_clause = self._build_search_clause_sql(search, search_columns)
        
        sql_core = base_sql.strip()
        if isinstance(search_clause, str) and search_clause.strip() != "":
           
            if _re.search(r"\bWHERE\b", sql_core, flags=_re.IGNORECASE):
                sql_core += " AND " + search_clause
            else:
                print(12)
                print(search_clause)
                sql_core += " WHERE " + search_clause
      

        order_sql = ""
        safe_ob = self._safe_identifier_sql(order_by, allow_dot=True)
        if safe_ob:
            order_sql = f" ORDER BY {safe_ob} {'ASC' if order_asc else 'DESC'}"

        if not database:
            final_sql = sql_core + order_sql
            rs = self.db.execute(text(final_sql), bind)
            return rs.mappings().all() or []
        

        count_sql = f"SELECT COUNT(*) AS cnt FROM ({sql_core}) AS _sub"
        total = self.db.execute(text(count_sql), bind).scalar() or 0

        offset = (page - 1) * rows
        data_sql = f"{sql_core}{order_sql} LIMIT :_limit OFFSET :_offset"
        bind_data = dict(bind, _limit=rows, _offset=offset)

        rs = self.db.execute(text(data_sql), bind_data)
        items = rs.mappings().all() or []

        total_pages = (total + rows - 1) // rows if rows else 0
        return {
            "list": items,
            "meta": {
                "page": page,
                "rows": rows,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            },
        }