import asyncio
import datetime
from typing import Optional, Tuple, Type

import aiocache
from aiocache import serializers


class AsyncioCacheManager:
    """This class manages cache.

    __init__ method by default uses SimpleMemoryCache and
    NullSerializer. Be careful, NullSerializer does not serialize the
    response and if the response is changed later it will affect the
    stored cached result.
    """

    def __init__(
        self,
        cache_class=aiocache.Cache.MEMORY,
        serializer=serializers.PickleSerializer(),
    ):
        self.cache = cache_class(serializer=serializer)

    async def run(
        self,
        f,
        *args,
        ttl: Optional[int],
        first_self=True,
        exceptions: Optional[Tuple[Type[Exception]]] = None,
        api_events_logging_service: Optional = None,
        message: Optional[str] = None,
        **kwargs,
    ):
        """This method allows running an async function with caching its
        results.

        Args:
            f (Callable): the async method to call
            ttl (int): the expiration time in seconds
            if ttl==None: return cache only if f failed, but cache the result every time
            exceptions: list of exceptions to catch in try(f)
            api_events_logging_service: logging service for project
            first_self (bool): pass False if the first argument is not self. Useful for class methods and static functions

        Returns:
            Any: either the cached result or the fetched one.
        """
        key = self.get_cache_key(f, first_self, args, kwargs)

        if ttl is not None:
            value = await self.get_from_cache(key)
            if value is not None:
                return value
        else:
            ttl = int(datetime.timedelta(weeks=1).total_seconds())

        try:
            result = await f(*args, **kwargs)
        except exceptions as e:
            return await self.get_from_cache(key, raise_exception=True)

        # do not wait for caching
        asyncio.create_task(self.set_in_cache(key, result, ttl=ttl))

        return result

    def get_cache_key(self, f, first_self, args, kwargs):
        return self._key_from_args(f, first_self, args, kwargs)

    def _key_from_args(self, func, first_self, args, kwargs):
        ordered_kwargs = sorted(kwargs.items())
        # use args[1:] since the first is 'self'
        return (
            (func.__module__ or "")
            + func.__name__
            + str(args[1:] if first_self else args)
            + str(ordered_kwargs)
        )

    async def get_from_cache(self, key, raise_exception=False):
        res = await self.cache.get(key)
        if not res and raise_exception:
            raise Exception("Cache Miss")
        return res

    async def set_in_cache(self, key, value, ttl):
        try:
            await self.cache.set(key, value, ttl=ttl)
        except Exception:
            pass
