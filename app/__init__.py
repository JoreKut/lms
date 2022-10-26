from fastapi import FastAPI
from app.configuration.server import Server


def create_app() -> FastAPI:
    app = FastAPI()
    return Server(app).get_app()
