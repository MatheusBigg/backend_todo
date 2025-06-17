from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def root():
    return {'message': 'Welcome to Skynet!'}


if __name__ == '__main__':
    root()
