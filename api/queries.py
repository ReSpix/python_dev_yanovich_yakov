from fastapi import Depends
import asyncpg
import db_conn

from exceptions import UserNotFoundException


async def get_user_id_by_login(login: str, connection: asyncpg.Connection) -> int:
    query = """
    SELECT
        id
    FROM users
        WHERE login = $1
    """
    result = await connection.fetchrow(query, login)
    if not result:
        raise UserNotFoundException(login)

    return result["id"]


async def get_comments_by_user_id(user_id: int, connection: asyncpg.Connection):
    query = """
    SELECT
        u.login commentator_login,
        p.header,
        ua.login author_login,
        COUNT(p.id) comment_count
    FROM comment c
        JOIN post p ON p.id = c.post_id
        JOIN users u ON u.id = c.commentator_id
        JOIN users ua ON ua.id = p.author_id
    WHERE
        u.id = $1
    GROUP BY
        p.id,
        u.id,
        ua.id
    """
    result = await connection.fetch(query, user_id)
    return result


async def get_general_logs_by_user_id(
    user_id: int, connection: asyncpg.Connection
) -> list:
    query = """
    SELECT 
        date(datetime) as date,
        SUM(CASE WHEN event_type_id = 1 THEN 1 ELSE 0 END) AS logins,
        SUM(CASE WHEN event_type_id = 5 THEN 1 ELSE 0 END) AS logouts,
        SUM(CASE WHEN space_type_id = 2 THEN 1 ELSE 0 END) AS blog_events
    FROM logs
    WHERE 
        user_id = $1
    GROUP BY date
    """
    data = await connection.fetch(query, user_id)

    return data
