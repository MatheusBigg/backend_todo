from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='testuser',
            email='KkR1o@example.com',
            password='testpassword',
        )
        session.add(new_user)
        await session.commit()
        user = await session.scalar(
            select(User).where(User.username == 'testuser')
        )

    assert asdict(user) == {
        'id': 1,
        'username': 'testuser',
        'email': 'KkR1o@example.com',
        'password': 'testpassword',
        'created_at': time,
        'updated_at': time,
    }
