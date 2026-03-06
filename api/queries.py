import asyncpg
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from db.models.authors import User, Post, Comment

from db.models.logs import Logs
from exceptions import UserNotFoundException


async def get_user_id_by_login(login: str, session: AsyncSession) -> int:
    query = select(User.id).where(User.login == login)
    result = await session.execute(query)
    user_id = result.scalar_one_or_none()

    if user_id is None:
        raise UserNotFoundException(login)

    return user_id


async def get_comments_by_user_id(user_id: int, session: AsyncSession):
    Author = aliased(User)
    query = (
        select(
            User.login.label("commentator_login"),
            Post.header,
            Author.login.label("author_login"),
            func.count(Post.id).label("comment_count"),
        )
        .select_from(Comment)
        .join(Post, Post.id == Comment.post_id)
        .join(User, User.id == Comment.commentator_id)
        .join(Author, Author.id == Post.author_id)
        .where(User.id == user_id)
        .group_by(Post.id, User.id, Author.id)
    )

    result = await session.execute(query)
    rows = result.all()
    return [dict(row._mapping) for row in rows]


async def get_general_logs_by_user_id(user_id: int, session: AsyncSession):
    query = (
        select(
            func.date(Logs.datetime).label("date"),
            func.sum(case((Logs.event_type_id == 1, 1), else_=0)).label("logins"),
            func.sum(case((Logs.event_type_id == 5, 1), else_=0)).label("logouts"),
            func.sum(case((Logs.space_type_id == 2, 1), else_=0)).label("blog_events"),
        )
        .where(Logs.user_id == user_id)
        .group_by(func.date(Logs.datetime))
    )
    result = await session.execute(query)
    rows = result.all()
    return [dict(row._mapping) for row in rows]
