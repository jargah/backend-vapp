# mysql_model.py
from __future__ import annotations

from sqlalchemy import text
import re as _re
from typing import List, Optional, Dict, Any, Tuple


class MySQLModel:
    def __init__(self, db, table: str):
        self.db = db
        self.table = table
        self.datatable_col_names: List[str] = []
        # Estado interno de transacción
        self._tx = None

    # ----------------------------
    # Utilidades internas
    # ----------------------------
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
        params: Dict[str, Any] = {}
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
            # OJO: concatena el search directamente (tal como tu versión original)
            parts.append(f"{col} LIKE '%{search}%'")

        if not parts:
            return "", params

        return " (" + " OR ".join(parts) + ") "

    # ----------------------------
    # NUEVO: Query genérica
    # ----------------------------
    async def query(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
        mappings: bool = True,
        fetch: str = "all",   # "all" | "one" | "scalar" | "none"
        debug: bool = False,
    ):
        """
        Ejecuta SQL con parámetros enlazados (:name).
        - mappings=True -> dict-like rows (Result.mappings()) si hay columnas.
        - fetch:
            "all"    -> lista de filas
            "one"    -> una fila
            "scalar" -> un valor escalar
            "none"   -> no hace fetch (INSERT/UPDATE/DELETE)
        """
        stmt = text(sql)
        bind = params or {}

        if debug:
            print("[SQL]", sql)
            print("[PARAMS]", bind)

        res = self.db.execute(stmt, bind)

        if fetch == "none":
            # Útil para INSERT/UPDATE/DELETE. Si necesitas rowcount:
            return getattr(res, "rowcount", None)

        # Primero el caso escalar
        if fetch == "scalar":
            val = res.scalar()
            if debug:
                print("[SCALAR]", val)
            return val

        # Si no devuelve filas (p.ej. DDL o DML sin RETURNING), corta aquí
        if not getattr(res, "returns_rows", False):
            if debug:
                print("[NO ROWS RETURNED]")
            return [] if fetch == "all" else None

        # Hay filas: intentar como mappings (dict-like). Si falla, usar tuplas.
        if mappings:
            try:
                if fetch == "all":
                    rows = res.mappings().all()
                    if debug:
                        print(f"[ROWS mappings all] n={len(rows)}")    
                    return rows
                if fetch == "one":
                    row = res.mappings().fetchone()
                    if debug:
                        print(f"[ROW mappings one] {row}")
                    return row
            except Exception as e:
                if debug:
                    print("[MAPPINGS FAILED]", e)
        
        if fetch == "all":
            rows = res.fetchall()
            if debug:
                print(f"[ROWS tuples all] n={len(rows)}")
                
            return rows
        if fetch == "one":
            row = res.fetchone()
            if debug:
                print(f"[ROW tuples one] {row}")
            return row

        return None

    # ----------------------------
    # NUEVO: Manejo de transacciones
    # ----------------------------
    def beginTransaction(self):
        """
        Inicia una transacción explícita (compatible con Session y Connection).
        No anida transacciones: si ya hay una abierta, no hace nada.
        """
        if self._tx is not None:
            return
        self._tx = self.db.begin()

    def commit(self):
        """
        Confirma la transacción si está abierta.
        """
        if self._tx is None:
            return
        committed = False
        try:
            self._tx.commit()
            committed = True
        except AttributeError:
            pass
        if not committed:
            # Fallback por si el objeto soporta commit directo
            self.db.commit()
        self._tx = None

    def rollback(self):
        """
        Revierte la transacción si está abierta.
        """
        if self._tx is None:
            return
        rolled = False
        try:
            self._tx.rollback()
            rolled = True
        except AttributeError:
            pass
        if not rolled:
            self.db.rollback()
        self._tx = None

    # ----------------------------
    # CRUD simples (siguen tu estilo)
    # ----------------------------
    async def insert(self, data: dict):
        columns = ", ".join(data.keys())
        values = ""
        for value in data.values():
            if isinstance(value, str) and value.find("TO_DATE") != -1:
                values += f"{value}, "
            elif isinstance(value, str) and value.find("TO_TIMESTAMP") != -1:
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
        # Nota: en algunos drivers MySQL result.lastrowid puede variar
        return getattr(result, "lastrowid", None)

    async def update(self, where: str, data: dict):
        set_values = ""
        for column, value in data.items():
            if isinstance(value, str) and value.find("TO_DATE") != -1:
                set_values += f"{column} = {value}, "
            elif isinstance(value, str) and value.find("TO_TIMESTAMP") != -1:
                set_values += f"{column} = {value}, "
            elif isinstance(value, str):
                set_values += f"{column} = '{value}', "
            else:
                set_values += f"{column} = {value}, "

        set_values = set_values[:-2]  # quitar última coma
        sql = f"UPDATE {self.table} SET {set_values} WHERE {where}"
        print(sql)

        result = self.db.execute(text(sql))
        self.db.commit()
        return result.rowcount

    # ----------------------------
    # SELECT helpers
    # ----------------------------
    async def featchAllRows(self):
        sql = f"SELECT * FROM {self.table}"
        return await self.db.query(sql)

    async def selectAll(self, where: str = "", order: str = "ASC", fields: Optional[str] = None):
        try:
            internal_fields = "*" if fields is None else fields
            sql = f"SELECT {internal_fields} FROM {self.table}"
            if where != "":
                sql += f" WHERE {where}"

            if order == "ASC":
                sql += " ORDER BY 1 ASC"
            elif order == "DESC":
                sql += " ORDER BY 1 DESC"

            query_stmt = text(sql)
            result = self.db.execute(query_stmt)
            result = result.mappings().all()
            if result is None:
                return None

            data: List[Dict[str, Any]] = []
            for row in result:
                data.append(row)
            return data
        except (ValueError, TypeError) as e:
            print(e)
            return None

    async def selectFirst(self, where: str = "", order: str = "ASC", fields: Optional[str] = None):
        try:
            internal_fields = "*" if fields is None else fields
            sql = f"SELECT {internal_fields} FROM {self.table}"
            if where != "":
                sql += f" WHERE {where}"

            if order == "ASC":
                sql += " ORDER BY 1 ASC"
            elif order == "DESC":
                sql += " ORDER BY 1 DESC"

            query_stmt = text(sql)
            result = self.db.execute(query_stmt)
            result = result.mappings().fetchone()

            if result is None:
                return None

            return result
        except (ValueError, TypeError) as e:
            print("error")
            print(e)
            return None

    # ----------------------------
    # Datatable
    # ----------------------------
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
        bind: Dict[str, Any] = {}

        # Si quieres forzar columnas desde fuera, asigna self.datatable_col_names antes
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
            if _re.search(r"\bWHERE\b", sql_core, flags[_re.IGNORECASE]):
                sql_core += " AND " + search_clause
            else:
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
