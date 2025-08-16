import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from middlewares.error_handler import ErrorHandler
from middlewares.database import Database
from api.routes import router
from helpers.routing import setRoutes

load_dotenv()

app = FastAPI()
app.title = os.getenv('APP_NAME')
app.version = '1.0.0'
app.add_middleware(ErrorHandler)
app.add_middleware(Database)

setRoutes(app, router)

@app.get('/', tags=['home'])
def root():
    return HTMLResponse('<h1>SOCIAL HELP KIT</h1>')

