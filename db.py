from __future__ import annotations

import os
from pathlib import Path
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Use DATABASE_URL env var; fallback to local SQLite file (dev-friendly)
BASE_DIR = Path(__file__).resolve().parent
SQLITE_PATH = (BASE_DIR / "cerrado.db").resolve()
SQLITE_URL = f"sqlite:///{SQLITE_PATH.as_posix()}"

DATABASE_URL = os.getenv("DATABASE_URL", SQLITE_URL)

# Engine: echo can be toggled with SQLALCHEMY_ECHO env
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("SQLALCHEMY_ECHO", "0") == "1",
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Dev-friendly: cria tabelas que não existirem
try:
    Base.metadata.create_all(engine)
except Exception:
    # Em produção, normalmente usamos migrações; ignorar caso falhe aqui
    pass

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
