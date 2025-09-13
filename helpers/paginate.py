from fastapi import Query, Request
from typing import Optional
from pydantic import BaseModel


class PaginationParams(BaseModel):
    database: bool = True
    page: int = 1
    rows: int = 10
    search: Optional[str] = None
    order_by: Optional[str] = None
    order_asc: bool = True


async def pagination_params(
    database: bool = Query(True, description="Query database or return all"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    rows: int = Query(10, ge=1, le=200, description="Number of rows"),
    search: Optional[str] = Query(None, description="Search keyword"),
    order_by: Optional[str] = Query(None, description="Order by field"),
    order_asc: bool = Query(True, description="Ascending order?"),
) -> PaginationParams:
    return PaginationParams(
        database=database,
        page=page,
        rows=rows,
        search=search,
        order_by=order_by,
        order_asc=order_asc,
    )


def build_links(request: Request, page: int, rows: int, has_prev: bool, has_next: bool):
    q = dict(request.query_params)
    q["rows"] = str(rows)
    next_url = prev_url = None
    
    if has_next:
        q["page"] = str(page + 1)
        next_url = str(request.url.replace_query_params(**q))
    
    if has_prev:
        q["page"] = str(page - 1)
        prev_url = str(request.url.replace_query_params(**q))
        
    return next_url, prev_url