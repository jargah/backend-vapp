from pydantic import BaseModel
from schemas.database import DatabaseConfig
from schemas.quadrum import QuadrumAPIScheme
from schemas.truora import TruoraScheme

class ConfigurationScheme(BaseModel):
    database: DatabaseConfig
    truora: TruoraScheme
    quadrum: QuadrumAPIScheme
    