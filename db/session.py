from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_settings


@lru_cache(maxsize=1)
def get_engine():
    settings = get_settings()
    connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
    return create_engine(settings.database_url, future=True, pool_pre_ping=True, connect_args=connect_args)


SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, future=True)
