from http import HTTPStatus

from fastapi import FastAPI

from app.api.V1.routers import auth, users
from app.schemas.schemas import Message

app = FastAPI(title='Skynet', version='1.0.0', description='API for my bots!')

app.include_router(auth.router)

app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def root():
    return {'message': 'Welcome to Skynet!'}
