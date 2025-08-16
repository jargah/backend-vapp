from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from database.MySQL import MySQL
class Database(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:

            mysql = MySQL()
            connection = await mysql.connect()
            if connection == None:
                raise HTTPException(
                    status_code=500,
                    detail='error_connection_database'
                )
            
            request.state.mysql = mysql

            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)})

    