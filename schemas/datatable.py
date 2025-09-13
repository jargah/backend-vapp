from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Query, Depends

class DataTableQueryDTO(BaseModel):
    database: bool = Field(default=True, description="False = sin paginación (regresa lista completa)")
    page: int = Field(default=1, ge=1)
    rows: int = Field(default=10, ge=1)
    search: Optional[str] = Field(default=None, description="Vacío/omitido = sin filtro")
    order_by: Optional[str] = Field(default=None, description="Nombre de campo o alias SQL")
    order_asc: bool = Field(default=True)

def datatable_query_dependency(
    database: bool = Query(True, description="False = sin paginación"),
    page: int = Query(1, ge=1),
    rows: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    order_by: Optional[str] = Query(None),
    order_asc: bool = Query(True),
) -> DataTableQueryDTO:
    if isinstance(search, str) and not search.strip():
        search = None
    return DataTableQueryDTO(
        database=database,
        page=page,
        rows=rows,
        search=search,
        order_by=order_by,
        order_asc=order_asc,
    )