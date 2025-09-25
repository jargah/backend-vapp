import json 
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