from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, StringConstraints

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
NonEmptyPassword = Annotated[str, StringConstraints(strip_whitespace=True, min_length=8)]

class LoginDTO(BaseModel):
    username: NonEmptyStr = Field()
    password: NonEmptyPassword = Field(min_length=8)

    class Config:
        json_schema_extra = {
            'example': {
                'username': 'test@test.com',
                'password': '12345678'
            }
        }