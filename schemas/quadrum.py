from typing import Optional
from pydantic import BaseModel, Field, constr, validator

NonEmptyStr = constr(min_length=1, strip_whitespace=True)

class QuadrumAPIConfigScheme(BaseModel):
    api: str
    contentType: Optional[NonEmptyStr] = Field(...)
    action: str
    

class QuadrumAPIScheme(BaseModel):
    register: QuadrumAPIConfigScheme
    timbrar: QuadrumAPIConfigScheme


class QuadrumScheme(BaseModel):
    username: str
    password: str
    register: QuadrumAPIScheme
    