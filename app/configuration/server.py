from typing import TypeVar

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configuration import __containers__
from ..internal.routes import __routes__

__all__ = ["Server"]

FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class Server:
    """Create server instance."""

    def __init__(self, app: FastAPI):
        self.__app = app
        self._register_services(app)
        self._register_routes(app)
        self._register_events(app)
        self._register_middlewares(app)
        self._register_http_exceptions(app)
        self.__register_cors_origins(app)

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def _register_events(app: FastAPI):
        from .events import on_startup
        app.on_event("startup")(on_startup)

    @staticmethod
    def _register_routes(app: FastAPI):
        __routes__.register_routes(app)

    @staticmethod
    def _register_services(app: FastAPI):
        __containers__.wire_packages(app=app)

    @staticmethod
    def __register_cors_origins(app: FastAPIInstance):
        """Register cors origins."""

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @staticmethod
    def _register_middlewares(app: FastAPI):
        pass

    @staticmethod
    def _register_http_exceptions(app: FastAPI):
        pass
