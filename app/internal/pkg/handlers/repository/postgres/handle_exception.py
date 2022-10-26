from typing import Callable

from psycopg2 import Error as QueryError
from psycopg2 import errorcodes

from app.pkg.models.base import Model
from app.internal.repository.exceptions import (
    CheckViolation,
    DriverError,
    ForeignKeyViolation,
    NumericValueOutOfRange,
    UniqueViolation,
)


def handle_exception(func: Callable[..., Model]):
    """Decorator Catching PostgreSQL Query Exceptions.

    Args:
        func: callable function object

    Returns:
        Result of call function.
    Raises:
        UniqueViolation: The query violates the domain uniqueness constraints
            of the database set
        DriverError: Invalid database query
        CheckViolation: Input or calculated values violate check constraint
    """

    async def wrapper(*args: object, **kwargs: object) -> Model:
        try:
            return await func(*args, **kwargs)
        except QueryError as e:
            if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                raise UniqueViolation
            elif e.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
                raise ForeignKeyViolation
            elif e.pgcode == errorcodes.CHECK_VIOLATION:
                raise CheckViolation
            elif e.pgcode == errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                raise NumericValueOutOfRange

            print(e)
            raise DriverError(message=e.pgerror)

    return wrapper
