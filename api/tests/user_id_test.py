import pytest
import pytest_asyncio
from sqlalchemy import insert
from db.models.authors import User
from exceptions import UserNotFoundException
from queries import get_user_id_by_login

@pytest_asyncio.fixture
async def setup_users(session):
    async def _create_users(logs_data):
        for data in logs_data:
            await session.execute(insert(User).values(**data))
        await session.commit()
    return _create_users

@pytest.mark.asyncio
async def test_get_user_id_by_login_exists(session, setup_users):
    real_login = "user1"
    users = [{"id": 1, "login": real_login}, {"id": 2, "login": "user2"}]
    
    await setup_users(users)
    
    result = await get_user_id_by_login(real_login, session)
    
    assert result is not None
    assert isinstance(result, int)
    assert result == 1

@pytest.mark.asyncio
async def test_get_user_id_by_login_not_found(session, setup_users):
    fake_login = "nonexistent_user"
    users = [{"id": 1, "login": "user1"}]
    
    await setup_users(users)
    
    with pytest.raises(UserNotFoundException) as exc_info:
        await get_user_id_by_login(fake_login, session)
    
    assert exc_info.value.login == fake_login