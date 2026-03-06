from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy import insert

from db.models.logs import Logs, SpaceType, EventType

from queries import get_general_logs_by_user_id


@pytest_asyncio.fixture
async def setup_logs(session):
    async def _create_logs(logs_data):
        space_types = [{"name": "global"}, {"name": "blog"}, {"name": "post"}]
        event_types = [
            {"name": "login"},
            {"name": "comment"},
            {"name": "create_post"},
            {"name": "delete_post"},
            {"name": "logout"},
        ]
        for space_type in space_types:
            await session.execute(insert(SpaceType).values(**space_type))

        for event_type in event_types:
            await session.execute(insert(EventType).values(**event_type))

        for data in logs_data:
            await session.execute(insert(Logs).values(**data))
        await session.commit()

    return _create_logs


@pytest.mark.asyncio
async def test_general_logs(session, setup_logs):
    user_id = 1

    logs_data = [
        {
            "user_id": user_id,
            "space_type_id": 1,
            "event_type_id": 1,
            "datetime": datetime(2026, 1, 1, 10, 0),
        },
        {
            "user_id": user_id,
            "space_type_id": 1,
            "event_type_id": 1,
            "datetime": datetime(2026, 1, 1, 12, 0),
        },
        {
            "user_id": user_id,
            "space_type_id": 1,
            "event_type_id": 5,
            "datetime": datetime(2026, 1, 1, 18, 0),
        },
        {
            "user_id": user_id,
            "space_type_id": 2,
            "event_type_id": 3,
            "datetime": datetime(2026, 1, 2, 10, 0),
        },
    ]

    await setup_logs(logs_data)

    result = await get_general_logs_by_user_id(user_id, session)
    assert result == [
        {"date": "2026-01-01", "logins": 2, "logouts": 1, "blog_events": 0},
        {"date": "2026-01-02", "logins": 0, "logouts": 0, "blog_events": 1},
    ]


@pytest.mark.asyncio
async def test_general_logs_empty(session):
    no_user_id = 999
    empty_result = await get_general_logs_by_user_id(no_user_id, session)
    assert empty_result == []


@pytest.mark.asyncio
async def test_general_logs_users_not_mixing(session, setup_logs):
    first_user_id = 1
    second_user_id = 2

    logs_data = [
        {
            "user_id": first_user_id,
            "space_type_id": 1,
            "event_type_id": 1,
            "datetime": datetime(2026, 1, 1, 10, 0),
        },
        {
            "user_id": second_user_id,
            "space_type_id": 1,
            "event_type_id": 1,
            "datetime": datetime(2026, 1, 1, 12, 0),
        }
    ]

    await setup_logs(logs_data)

    result = await get_general_logs_by_user_id(first_user_id, session)
    assert result == [
        {"date": "2026-01-01", "logins": 1, "logouts": 0, "blog_events": 0},
    ]

    result = await get_general_logs_by_user_id(second_user_id, session)
    assert result == [
        {"date": "2026-01-01", "logins": 1, "logouts": 0, "blog_events": 0},
    ]