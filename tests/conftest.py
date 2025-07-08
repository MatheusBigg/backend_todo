from contextlib import contextmanager
from datetime import datetime
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.security import get_password_hash
from app.core.settings import Settings
from app.db.database import get_session
from app.main import app
from app.models.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(  # Cria conexao com o db
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)  # Cria as tabelas no db

    with Session(engine) as session:
        yield session  # abre sessao de conexao entro o codigo e o db

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    password = 'testpassword'
    user = User(
        username='testuser',
        email='KkR1o@example.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/api/v1/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.OK
    return response.json()['access_token']


@pytest.fixture
def settings():
    return Settings()
