from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response, routing
from fastapi.responses import JSONResponse
from api.account.routes import account_router

class Routes(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) ->  Response | JSONResponse:
        try:

            for route in account_router:
                print(route)
                routing.APIRouter().include_router(router=route)

            return await call_next(request)
        except Exception as err:
            return JSONResponse(status_code=500, content={'error': str(err)})