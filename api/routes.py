from fastapi import Depends
from fastapi.routing import APIRouter
import asyncpg
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from db import connection
from db.connection import DatabaseName
import queries


api_router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@api_router.get("/comments")
async def comments_dataset(
    login: str,
    connection: AsyncSession = Depends(connection.get_db(DatabaseName.AUTHORS)),
):
    user_id = await queries.get_user_id_by_login(login, connection)
    data = await queries.get_comments_by_user_id(user_id, connection)
    return data


@api_router.get("/general")
async def general_dataset(
    login: str,
    authors_conn: AsyncSession = Depends(connection.get_db(DatabaseName.AUTHORS)),
    logs_conn: AsyncSession = Depends(connection.get_db(DatabaseName.LOGS)),
):
    user_id = await queries.get_user_id_by_login(login, authors_conn)
    data = await queries.get_general_logs_by_user_id(user_id, logs_conn)
    return data


@api_router.get("/user-list")
async def user_list(
    connection: AsyncSession = Depends(connection.get_db(DatabaseName.AUTHORS)),
):
    data = await queries.get_all_users(connection)
    return data
