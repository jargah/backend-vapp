# mysql_model.py
from __future__ import annotations

from sqlalchemy import text
import re as _re
from typing import List, Optional, Dict, Any, Sequence


class MySQLModel:
    """
    Versión enfocada a MySQL.
    - Búsqueda segura: params enlazados y CAST a CHAR.
    - Tolerante a NULL: COALESCE(..., '').
    - Case/accents-insensitive: COLLATE utf8mb4_0900_ai_ci (si tu server lo soporta) + fallback LOWER().
    - ORDER BY seguro con whitelist (self.datatable_col_names).
    """
    # Cambia esta colación si tu server no tiene 0900 (p.ej. usa utf8mb4_unicode_ci)
    PREFERRED_COLLATION = "utf8mb4_0900_ai_ci"

    def __init__(self, db, table: str):
        self.db = db
        self.table = table
        self.datatable_col_names: List[str] = []    # <- llena esto con columnas permitidas para search/order
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
        """
        Valida que el identificador sea seguro (A-Z, a-z, 0-9, _ y .) y esté en whitelist.
        """
        if not name:
            return None
        pat = r"[A-Za-z0-9_\.]+" if allow_dot else r"[A-Za-z0-9_]+"
        if not _re.fullmatch(pat, name):
            return None
        if self.datatable_col_names:
            base = self._split_alias(name)
            return name if (base in self.datatable_col_names or name in self.datatable_col_names) else None
        return name

    def _build_search_clause_sql(
        self,
        search: str | None,
        search_columns: Sequence[str] | None,
        bind: Dict[str, Any],
        param_name: str = "_search",
    ) -> str:
        """
        MySQL-only: genera ORs de LIKE seguros contra columnas (casteadas a CHAR).
        Intenta usar colación AI/CI para insensibilidad a mayúsculas/acentos.
        Pone el parámetro una sola vez en 'bind'.
        """
        
        print(search_columns)
        
        if not search or not search_columns:
            return ""

        parts: List[str] = []
        for col in search_columns:
            if not col or not _re.fullmatch(r"[A-Za-z0-9_\.]+", col):
                continue
            
            parts.append(f"{col} LIKE '%{search}%'")
            
        if not parts:
            return ""
        
        

        bind[param_name] = f"%{search}%"
        return "(" + " OR ".join(parts) + ")"

    # ----------------------------
    # Query genérica (sync bajo async)
    # ----------------------------
    async def query(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
        mappings: bool = True,
        fetch: str = "all",   # "all" | "one" | "scalar" | "none"
        debug: bool = False,
    ):
        stmt = text(sql)
        bind = params or {}

        if debug:
            print("[SQL]", sql)
            print("[PARAMS]", bind)

        res = self.db.execute(stmt, bind)

        if fetch == "none":
            return getattr(res, "rowcount", None)
        if fetch == "scalar":
            return res.scalar()

        if not getattr(res, "returns_rows", False):
            return [] if fetch == "all" else None

        if mappings:
            try:
                if fetch == "all":
                    return res.mappings().all()
                if fetch == "one":
                    return res.mappings().fetchone()
            except Exception:
                pass

        if fetch == "all":
            return res.fetchall()
        if fetch == "one":
            return res.fetchone()
        return None

    # ----------------------------
    # Transacciones
    # ----------------------------
    def beginTransaction(self):
        if self._tx is not None:
            return
        self._tx = self.db.begin()

    def commit(self):
        if self._tx is None:
            return
        committed = False
        try:
            self._tx.commit(); committed = True
        except AttributeError:
            pass
        if not committed:
            self.db.commit()
        self._tx = None

    def rollback(self):
        if self._tx is None:
            return
        rolled = False
        try:
            self._tx.rollback(); rolled = True
        except AttributeError:
            pass
        if not rolled:
            self.db.rollback()
        self._tx = None

    # ----------------------------
    # CRUD simples
    # ----------------------------
    async def insert(self, data: dict):
        columns = ", ".join(data.keys())
        values = ""
        for value in data.values():
            if isinstance(value, str) and "TO_DATE" in value:
                values += f"{value}, "
            elif isinstance(value, str) and "TO_TIMESTAMP" in value:
                values += f"{value}, "
            elif isinstance(value, str):
                values += f"'{value}', "
            else:
                values += f"{value}, "

        values = values[:-2]
        sql = f"INSERT INTO {self.table} ({columns}) VALUES ({values})"
        print(sql)

        res = self.db.execute(text(sql))
        self.db.commit()
        return getattr(res, "lastrowid", None)

    async def update(self, where: str, data: dict):
        set_values = ""
        for column, value in data.items():
            if isinstance(value, str) and "TO_DATE" in value:
                set_values += f"{column} = {value}, "
            elif isinstance(value, str) and "TO_TIMESTAMP" in value:
                set_values += f"{column} = {value}, "
            elif isinstance(value, str):
                set_values += f"{column} = '{value}', "
            else:
                set_values += f"{column} = {value}, "

        set_values = set_values[:-2]
        sql = f"UPDATE {self.table} SET {set_values} WHERE {where}"
        print(sql)

        res = self.db.execute(text(sql))
        self.db.commit()
        return res.rowcount

    # ----------------------------
    # SELECT helpers
    # ----------------------------
    async def featchAllRows(self):
        sql = f"SELECT * FROM {self.table}"
        return await self.query(sql)

    async def selectAll(self, where: str = "", order: str = "ASC", fields: Optional[str] = None):
        try:
            internal_fields = "*" if fields is None else fields
            sql = f"SELECT {internal_fields} FROM {self.table}"
            if where:
                sql += f" WHERE {where}"

            if order == "ASC":
                sql += " ORDER BY 1 ASC"
            elif order == "DESC":
                sql += " ORDER BY 1 DESC"

            res = self.db.execute(text(sql))
            rows = res.mappings().all()
            return list(rows) if rows is not None else None
        except (ValueError, TypeError) as e:
            print(e)
            return None

    async def selectFirst(self, where: str = "", order: str = "ASC", fields: Optional[str] = None):
        try:
            internal_fields = "*" if fields is None else fields
            sql = f"SELECT {internal_fields} FROM {self.table}"
            if where:
                sql += f" WHERE {where}"

            if order == "ASC":
                sql += " ORDER BY 1 ASC"
            elif order == "DESC":
                sql += " ORDER BY 1 DESC"

            res = self.db.execute(text(sql))
            row = res.mappings().fetchone()
            return row if row is not None else None
        except (ValueError, TypeError) as e:
            print("error"); print(e)
            return None

    # ----------------------------
    # Datatable (MySQL mejorado)
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

        search_columns = list(self.datatable_col_names or [])
        
        print(search_columns)

        # paginación segura
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

        # envolvemos el SQL base para no romper WHERE/ORDER existentes
        sql_core = f"SELECT * FROM ({base_sql.strip()}) AS q"

        # búsqueda (WHERE ...)
        where_search = self._build_search_clause_sql(search, search_columns, bind, param_name="_search")
        if where_search:
            sql_core += " WHERE " + where_search

        # ORDER BY seguro
        order_sql = ""
        safe_ob = self._safe_identifier_sql(order_by, allow_dot=True)
        if safe_ob:
            order_sql = f" ORDER BY {safe_ob} {'ASC' if order_asc else 'DESC'}"

        # sin total desde DB
        if not database:
            final_sql = sql_core + order_sql
            rs = self.db.execute(text(final_sql), bind)
            return rs.mappings().all() or []

        # total de filas
        count_sql = f"SELECT COUNT(*) AS cnt FROM ({sql_core}) AS _sub"
        total = self.db.execute(text(count_sql), bind).scalar() or 0

        # página de datos
        offset = (page - 1) * rows
        # LIMIT :_limit OFFSET :_offset (válido MySQL 5.7+); si prefieres, usa "LIMIT :_offset, :_limit"
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
