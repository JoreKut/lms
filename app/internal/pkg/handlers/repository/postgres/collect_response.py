import datetime
import functools
from functools import wraps
from typing import List, Union

import pydantic
from psycopg2.extras import RealDictRow

from app.pkg.models.base import Model
from app.internal.repository.exceptions import EmptyResult
from app.pkg.cache import AsyncioCacheManager

from .handle_exception import handle_exception

cache = AsyncioCacheManager()


def collect_response(
    fn=None,
    convert_to_pydantic=True,
    cache_for: datetime.timedelta = None,
    nullable=False,
    clear_cache=False,
    key=None,
):
    # fn is None when params for decorator are provided
    if fn is None:
        return functools.partial(
            collect_response,
            convert_to_pydantic=convert_to_pydantic,
            cache_for=cache_for,
            nullable=nullable,
            clear_cache=clear_cache,
            key=key,
        )

    @wraps(fn)
    @handle_exception
    async def inner(*args: object, **kwargs: object) -> Union[List[Model], Model, None]:
        if clear_cache:
            await cache.clear_cache(key=key)

        if cache_for is not None:
            # cache some responses
            response = await cache.run(fn, *args, ttl=cache_for.seconds, **kwargs)
        else:
            response = await fn(*args, **kwargs)

        if response is True:
            return response

        if response is None:
            # some responses are empty lists we should allow them.
            # isinstance cannot digest List[int], only List, so __origin__ is used

            if "return" in fn.__annotations__:
                return_class = fn.__annotations__["return"]
                if hasattr(return_class, "__origin__"):
                    return_class = return_class.__origin__
                if isinstance([], return_class):
                    return []
                if nullable:
                    return None

            raise EmptyResult

        if convert_to_pydantic:
            return pydantic.parse_obj_as(
                (ann := fn.__annotations__["return"]),
                await __convert_response(response=response, annotations=str(ann)),
            )

        return response

    return inner


async def __convert_response(response: RealDictRow, annotations: str):
    r = response.copy()
    if annotations.replace("typing.", "").startswith("List"):
        return [await __convert_memory_viewer(item) for item in r]
    return await __convert_memory_viewer(r)


async def __convert_memory_viewer(r: RealDictRow):
    for key, value in r.items():
        if isinstance(value, memoryview):
            r[key] = value.tobytes()
    return r
