from http import HTTPStatus

from fastapi import FastAPI

from app.schemas.schemas import Message

app = FastAPI(title='Skynet', version='1.0.0', description='API for my bots!')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def root():
    return {'message': 'Welcome to Skynet!'}
