from datetime import datetime

def now_formatted() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")