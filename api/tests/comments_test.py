import pytest
import pytest_asyncio
from sqlalchemy import insert
from db.models.authors import Blog, Post, User, Comment
from exceptions import UserNotFoundException
from queries import get_comments_by_user_id


@pytest_asyncio.fixture
async def setup_authors_database(session):
    async def _create_authors_database(tables: dict[type, list[dict]]):
        for table in tables:
            for data in tables[table]:
                await session.execute(insert(table).values(**data))
        await session.commit()

    return _create_authors_database


@pytest.mark.asyncio
async def test_get_comment_by_user_id(session, setup_authors_database):
    user_id = 2
    tables = {
        User: [{"id": 1, "login": "user1"}, {"id": user_id, "login": "user2"}],
        Blog: [{"id": 1, "owner_id": 1, "name": "Blog1"}],
        Post: [
            {"id": 1, "text": "post1", "header": "Header1", "author_id": 1, "blog_id": 1},
            {"id": 2, "text": "post2", "author_id": 1, "blog_id": 1},
        ],
        Comment: [
            {"id": 1, "commentator_id": 2, "text": "comment1", "post_id": 1},
            {"id": 2, "commentator_id": 2, "text": "comment2", "post_id": 1},
            {"id": 3, "commentator_id": 2, "text": "comment3", "post_id": 2},
        ]
    }

    await setup_authors_database(tables)

    result = await get_comments_by_user_id(user_id, session)

    assert result == [
        {
            "commentator_login": "user2",
            "header": "Header1",
            "author_login": "user1",
            "comment_count": 2,
        },
        {
            "commentator_login": "user2",
            "header": None,
            "author_login": "user1",
            "comment_count": 1,
        },
    ]

@pytest.mark.asyncio
async def test_get_comment_by_user_id_empty(session, setup_authors_database):
    user_id = 1

    result = await get_comments_by_user_id(user_id, session)

    assert result == []