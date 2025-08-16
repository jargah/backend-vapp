import jwt
import os
from fastapi.responses import JSONResponse

def create(payload: dict) -> str:
    print(os.getenv('JWT_TOKEN'))
    token: str = jwt.encode(payload=payload, key=os.getenv(), algorithm="HS256")
    return token

def decode(token: str) -> dict:
    try:
        key = os.getenv('JWT_TOKEN')
        data: dict = jwt.decode(token, key=key, algorithms=["HS256"])
        return data
    except jwt.ExpiredSignatureError as err:
        return None