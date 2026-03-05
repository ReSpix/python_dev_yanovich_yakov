from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
import asyncpg
import logging

from exceptions import UserNotFoundException
import db_conn
import queries


api_router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@api_router.get("/comments")
async def comments_dataset(
    connection: asyncpg.Connection = Depends(db_conn.get_db("authors_database")),
):
    pass


@api_router.get("/general")
async def general_dataset(
    login: str,
    authors_conn: asyncpg.Connection = Depends(db_conn.get_db("authors_database")),
    logs_conn: asyncpg.Connection = Depends(db_conn.get_db("logs_database")),
):
    try:
        user_id = await queries.get_user_id_by_login(login, authors_conn)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.to_dict())

    data = await queries.get_general_logs_by_user_id(user_id, logs_conn)
    return data
