from datetime import datetime, timedelta
from http import HTTPStatus

from jwt import decode, encode

from app.core.security import create_access_token
from app.core.settings import Settings


def test_jwt(settings):
    data = {'test': 'test'}
    token = create_access_token(data)
    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/api/v1/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


# Feito a parte
def test_jwt_no_subject_email(client):
    settings = Settings()

    # Create a token without the 'sub' claim, but with an 'exp' for validity
    to_encode = {}
    expire = datetime.now() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    # Encode the token without 'sub'
    token_without_sub = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    # Attempt to access a protected endpoint with this token
    response = client.delete(
        '/api/v1/users/1',
        headers={'Authorization': f'Bearer {token_without_sub}'},
    )

    # Assert that the response is UNAUTHORIZED due to missing subject email
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
