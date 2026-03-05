import asyncpg
import os
from typing import AsyncGenerator
import logging


logger = logging.getLogger(__name__)


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


_pools: dict[str, asyncpg.Pool] = {}


async def get_pool(db_name: str) -> asyncpg.Pool:
    if db_name not in _pools:
        await create_pool(db_name)

    return _pools[db_name]


async def create_pool(db_name: str):
    try:
        pool = await asyncpg.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=db_name,
            min_size=1,
            max_size=5,
        )
        _pools[db_name] = pool
        logger.info(f"Database pool created: {db_name}")
    except asyncpg.PostgresConnectionError:
        logger.error(f"Unable to connect: {db_name}")


async def close_pool(db_name):
    if db_name not in _pools:
        logger.warning(f"No such pool to close: {db_name}")
        return

    await _pools[db_name].close()
    logger.info(f"Database pool closed: {db_name}")
    _pools.pop(db_name)


async def close_all_pools():
    names = list(_pools.keys())
    for name in names:
        await close_pool(name)
    logger.info("All database pools closed")


def get_db(db_name: str):
    async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
        pool = await get_pool(db_name)
        conn = await pool.acquire()
        try:
            yield conn # type: ignore
        finally:
            await pool.release(conn)

    return get_db_connection
