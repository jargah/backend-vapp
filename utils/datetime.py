# datetime_utils.py
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from math import ceil as _ceil
from typing import Optional, Union

# ----------------------------
# Helpers internos
# ----------------------------

def _moment_to_strftime(fmt: str) -> str:
    """
    Convierte tokens comunes de moment a strftime.
    Soporta lo más usado del ejemplo. Amplía si necesitas más.
    """
    mapping = {
        "YYYY": "%Y",
        "YY": "%y",
        "MM": "%m",
        "DD": "%d",
        "HH": "%H",
        "mm": "%M",
        "ss": "%S",
        "ddd": "%a",  # Sun..Sat (inglés)
        "dddd": "%A", # Sunday..Saturday (inglés)
    }
    out = fmt
    for k, v in mapping.items():
        out = out.replace(k, v)
    return out

def _to_datetime(
    value: Union[datetime, str, int, float, None],
    tz: Optional[str] = None
) -> datetime:
    """
    Normaliza un valor a datetime aware (UTC o tz dada).
    Acepta:
      - datetime (naive => asume UTC)
      - str ISO o 'YYYY-MM-DD HH:mm:ss'
      - epoch seconds (int/float)
      - None => ahora
    """
    if value is None:
        dt = datetime.now(timezone.utc)
    elif isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    elif isinstance(value, (int, float)):  # epoch seconds
        dt = datetime.fromtimestamp(value, tz=timezone.utc)
    elif isinstance(value, str):
        s = value.strip()
        # Intento ISO
        try:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
            dt = dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            # Intento 'YYYY-MM-DD HH:mm:ss'
            try:
                dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            except ValueError:
                # Intento 'YYYY-MM-DD'
                dt = datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    else:
        raise TypeError("Unsupported datetime input type")

    if tz:
        return dt.astimezone(ZoneInfo(tz))
    return dt

# ----------------------------
# Formatos / ahora / timestamp
# ----------------------------

def now(fmt: str = "YYYY-MM-DD HH:mm:ss") -> str:
    return datetime.now(ZoneInfo("UTC")).strftime(_moment_to_strftime(fmt))

def timestamp(date: Union[datetime, str, int, float, None] = None) -> int:
    dt = _to_datetime(date)
    return int(dt.timestamp())

def date_format(date: Union[datetime, str, int, float], fmt: str = "YYYY-MM-DD HH:mm:ss") -> str:
    dt = _to_datetime(date)
    return dt.strftime(_moment_to_strftime(fmt))

def date_format_timezone(
    date: Union[datetime, str, int, float],
    tz: str,
    fmt: str = "YYYY-MM-DD HH:mm:ss"
) -> str:
    dt = _to_datetime(date, tz)
    return dt.strftime(_moment_to_strftime(fmt))

# ----------------------------
# Día/mes (nombres)
# ----------------------------

_DAYS_ES = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]
_DAYS_ES_FULL = ["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"]

def get_day(
    date: Union[datetime, str, int, float],
    lang: str = "es",
    signs: bool = True,  # quitar acentos si True
    long_name: bool = False
) -> str:
    dt = _to_datetime(date)
    idx = int(dt.strftime("%w"))  # 0=Dom ... 6=Sáb
    if lang == "es":
        day = _DAYS_ES_FULL[idx] if long_name else _DAYS_ES[idx]
        if signs:
            day = (day
                   .replace("á","a").replace("é","e")
                   .replace("í","i").replace("ó","o").replace("ú","u"))
        return day
    # fallback EN
    return dt.strftime("%A" if long_name else "%a")

def month_names_en() -> list[str]:
    return [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

def month_names_es() -> list[str]:
    return [
        "Enero","Febrero","Marzo","Abril","Mayo","Junio",
        "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
    ]

def get_month(
    date: Union[datetime, str, int, float],
    lang: str = "es",
    long_name: bool = True
) -> str:
    dt = _to_datetime(date)
    m = dt.month - 1
    if lang == "es":
        return month_names_es()[m]
    return month_names_en()[m]

# ----------------------------
# Diferencias
# ----------------------------

def difference_in_days(
    date1: Union[datetime, str, int, float],
    date2: Union[datetime, str, int, float, None] = None,
    ceil: bool = True
) -> float | int:
    d1 = _to_datetime(date1)
    d2 = _to_datetime(date2)
    days = (d2 - d1).total_seconds() / 86400.0
    return _ceil(days) if ceil else days

def difference_in_hours(
    date1: Union[datetime, str, int, float],
    date2: Union[datetime, str, int, float, None] = None,
    ceil: bool = True
) -> float | int:
    d1 = _to_datetime(date1)
    d2 = _to_datetime(date2)
    hours = (d2 - d1).total_seconds() / 3600.0
    return _ceil(hours) if ceil else hours

def difference_in_minutes(
    date1: Union[datetime, str, int, float],
    date2: Union[datetime, str, int, float, None] = None,
    ceil: bool = False
) -> float | int:
    d1 = _to_datetime(date1)
    d2 = _to_datetime(date2)
    minutes = (d2 - d1).total_seconds() / 60.0
    return _ceil(minutes) if ceil else minutes

# ----------------------------
# Sumas / Restas
# ----------------------------

def add_seconds(date: Union[datetime, str, int, float], seconds: Union[int, float]) -> datetime:
    return _to_datetime(date) + timedelta(seconds=float(seconds))

def add_minutes(date: Union[datetime, str, int, float], minutes: Union[int, float]) -> datetime:
    return _to_datetime(date) + timedelta(minutes=float(minutes))

def add_hours(date: Union[datetime, str, int, float], hours: Union[int, float]) -> datetime:
    return _to_datetime(date) + timedelta(hours=float(hours))

def add_days(date: Union[datetime, str, int, float], days: Union[int, float]) -> datetime:
    return _to_datetime(date) + timedelta(days=float(days))

def add_months(date: Union[datetime, str, int, float], months: int) -> datetime:
    """
    Suma meses de forma simple preservando día cuando es posible.
    Si el mes destino no tiene el mismo día (p. ej., 31 → febrero), recorta al último día del mes.
    """
    dt = _to_datetime(date)
    y = dt.year + (dt.month - 1 + months) // 12
    m = (dt.month - 1 + months) % 12 + 1
    # último día del mes destino
    last = last_day_month(y, m)
    d = min(dt.day, last)
    return dt.replace(year=y, month=m, day=d)

def add_years(date: Union[datetime, str, int, float], years: int) -> datetime:
    dt = _to_datetime(date)
    try:
        return dt.replace(year=dt.year + years)
    except ValueError:
        # 29-Feb a año no bisiesto → 28-Feb
        return dt.replace(month=2, day=28, year=dt.year + years)

def remove_days(date: Union[datetime, str, int, float], days: Union[int, float]) -> datetime:
    return add_days(date, -float(days))

def remove_minutes(date: Union[datetime, str, int, float], minutes: Union[int, float]) -> datetime:
    return add_minutes(date, -float(minutes))

def remove_months(date: Union[datetime, str, int, float], months: int) -> datetime:
    return add_months(date, -months)

def remove_years(date: Union[datetime, str, int, float], years: int) -> datetime:
    return add_years(date, -years)

# ----------------------------
# Otros
# ----------------------------

def last_day_month(year: int, month: int) -> int:
    """
    Devuelve el último día del mes (1..12).
    Tip: en Python, day=0 del mes siguiente es el último del mes actual.
    """
    if month == 12:
        nxt = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        nxt = datetime(year, month + 1, 1, tzinfo=timezone.utc)
    return (nxt - timedelta(days=1)).day

def seconds_from_time(time_str: str) -> int:
    """
    'HH:MM:SS' -> segundos totales.
    """
    hh, mm, ss = (int(x) for x in time_str.split(":"))
    return hh * 3600 + mm * 60 + ss
