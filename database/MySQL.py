from __future__ import annotations

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from configuration.config import configuration


DATABASE_URL: str = "mysql+mysqlconnector://{user}:{password}@{host}:3306/ven_app_api".format(
    user=configuration['database']['user'], 
    password=configuration['database']['password'],
    host=configuration['database']['host']
)
DB_ECHO: bool = os.getenv("DB_ECHO", "true").lower() in ("1", "true", "yes", "y")

engine: Engine = create_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    future=True,
    pool_pre_ping=True,
)

def get_engine() -> Engine:
    return engine


def get_db() -> Generator[Connection, None, None]:

    conn: Connection = engine.connect()
    try:
        yield conn
    finally:
        conn.close()


def ensure_tx(conn: Connection):
    if not conn.in_transaction():
        return conn.begin()
    return None


def commit_tx(conn: Connection, tx=None) -> None:
    if tx is not None:
        if tx.is_active:
            tx.commit()
        return
    cur = conn.get_transaction()
    if cur is not None and cur.is_active:
        conn.commit()


def rollback_tx(conn: Connection, tx=None) -> None:
    if tx is not None:
        if tx.is_active:
            tx.rollback()
        return
    if conn.in_transaction():
        conn.rollback()
