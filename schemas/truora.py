from pydantic import BaseModel


class TruoraAPIScheme(BaseModel):
    keys_url: str
    base_url: str
    result_url: str

class TruoraScheme(BaseModel):
    key: str
    flow: str
    api: TruoraAPIScheme
    