from http import HTTPStatus

from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to Skynet!'}
