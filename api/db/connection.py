from enum import Enum

import os
from typing import Any, AsyncGenerator
import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

logger = logging.getLogger(__name__)


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


class DatabaseName(str, Enum):
    AUTHORS = "authors_database"
    LOGS = "logs_database"


engines: dict[str, Any] = {}
session_factories: dict[str, async_sessionmaker] = {}


async def get_session_factory(name: DatabaseName) -> async_sessionmaker:
    if name.value not in session_factories:
        await create_session_factory(name.value)

    return session_factories[name.value]


async def init_db_engines():
    for name in [dn.value for dn in DatabaseName]:
        await create_session_factory(name)


async def create_session_factory(name: str):
    engines[name] = create_async_engine(
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{name}",
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )
    session_factories[name] = async_sessionmaker(
        bind=engines[name], autoflush=False, autocommit=False
    )


def get_db(db_name: DatabaseName):
    async def wrapper() -> AsyncGenerator[AsyncSession, None]:
        async with session_factories[db_name.value]() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    return wrapper
