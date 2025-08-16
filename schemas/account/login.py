from pydantic import BaseModel, Field

class AccountLoginSchema(BaseModel):
    username: str = Field()
    password: str = Field(min_length=8)

    class Config:
        json_schema_extra = {
            'example': {
                'username': 'test',
                'password': '12345678'
            }
        }