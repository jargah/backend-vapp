import json 
import re
import unicodedata
from fastapi import UploadFile

_slug_re = re.compile(r"[^a-zA-Z0-9._-]+")
MAX_BYTES = 5 * 1024 * 1024  # 5 MB

def parseDict(data: str):
    return json.loads(data)

def split_fullname(fullname: str) -> dict:
    parts = fullname.strip().split()
    
    first_name = ""
    last_name = ""
    second_surname = ""
    
    if not parts:
        return {"first_name": "", "last_name": "", "second_surname": ""}
    
    if len(parts) == 1:
        first_name = parts[0]
    elif len(parts) == 2:
        first_name, last_name = parts
    elif len(parts) == 3:
        first_name, last_name, second_surname = parts
    else:
        first_name = " ".join(parts[:-2])
        last_name = parts[-2]
        second_surname = parts[-1]
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "second_surname": second_surname
    }
    
    
def safe_filename(name: str) -> str:
    # normaliza, quita acentos, espacios -> _
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    name = name.replace(" ", "_")
    name = _slug_re.sub("", name)
    
    return name or "file"

async def size_guard(up: UploadFile, max_bytes: int = MAX_BYTES) -> int:
    total = 0
    await up.seek(0)
    while True:
        chunk = await up.read(1024 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            print(f"File '{up.filename}' too large (> {max_bytes} bytes)")
            return None
    await up.seek(0)
    return total


def calculate_max_bytes(megabytes: int) -> int:

    if megabytes <= 0:
        return None
    return megabytes * 1024 * 1024

def get_full_extension(filename: str) -> str:
    parts = filename.split(".")
    if len(parts) > 1:
        return ".".join(parts[1:]).lower()
    return ""