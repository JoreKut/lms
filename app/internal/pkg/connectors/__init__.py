from .iopostgres import MyPostgres
"""All connectors in declarative container."""

from dependency_injector import containers, providers
from .iopostgres import MyPostgres

__all__ = ["Connectors", "MyPostgres"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with connectors."""

    postgresql = providers.Factory(
        MyPostgres,
    )
