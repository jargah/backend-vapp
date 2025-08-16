from pydantic import BaseModel

class DatabaseConfig(BaseModel):
    host: str
    user: str
    password: str
    database: str
    port: int