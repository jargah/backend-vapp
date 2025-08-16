from fastapi import FastAPI

def setRoutes(app: FastAPI, routes: list) -> None:
    for route in routes:
        print(route)
        app.include_router(router=route)