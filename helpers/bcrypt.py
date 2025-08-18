# security/bcrypt.py
from __future__ import annotations
import os
from typing import Optional
from functools import lru_cache
import bcrypt


class Bcrypt:
    def __init__(self, rounds: int | None = None, pepper: Optional[str] = None) -> None:
        if rounds is not None and (rounds < 4 or rounds > 31):
            raise ValueError("bcrypt rounds debe estar entre 4 y 31.")
        self.rounds = rounds
        # Usa BCRYPT_PEPPER (secreto app-wide). El salt real lo genera bcrypt.gensalt().
        self.pepper = pepper or os.getenv("BCRYPT_PEPPER") or ""

    def _password_bytes(self, password: str) -> bytes:
        return (password + self.pepper).encode("utf-8")

    def hash(self, password: str) -> str:
        salt = bcrypt.gensalt() if self.rounds is None else bcrypt.gensalt(rounds=self.rounds)
        return bcrypt.hashpw(self._password_bytes(password), salt).decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(self._password_bytes(password), hashed.encode("utf-8"))
        except ValueError:
            return False

    def needs_rehash(self, hashed: str) -> bool:
        if self.rounds is None:
            return False
        try:
            cost = int(hashed.split("$")[2])
            return cost < self.rounds
        except Exception:
            return True


# --- Auto-inicio ---

def _parse_rounds(value: Optional[str]) -> Optional[int]:
    try:
        return int(value) if value is not None else None
    except ValueError:
        return None

BCRYPT = Bcrypt(
    rounds=_parse_rounds(os.getenv("BCRYPT_ROUNDS")),  
    pepper=os.getenv("BCRYPT_PEPPER"),
)

@lru_cache
def get_bcrypt() -> Bcrypt:
    return Bcrypt(
        rounds=_parse_rounds(os.getenv("BCRYPT_ROUNDS")),
        pepper=os.getenv("BCRYPT_PEPPER"),
    )
