from asyncio import EventLoop, get_event_loop
from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Any, Awaitable, Callable, Unpack
from diskcache import Cache
from httpx import Response

from kubeq.logging import sources

logger = sources.cache.logger


class AsyncCache:
    _thread_pool = ThreadPoolExecutor(max_workers=4)

    def __init__(self, cache: Cache):
        self._cache = cache

    async def _run_async[R](self, func: Callable[[Cache], R]) -> R:
        def _run():
            return func(self._cache)

        return await get_event_loop().run_in_executor(self._thread_pool, _run)

    async def get(self, key: str, **kwargs: Any):
        def _get(cache: Cache):
            result = cache.get(key, **kwargs)
            if result:
                logger.debug(f"Cache hit for {key}")
            else:
                logger.debug(f"Cache miss for {key}")
            return result

        return await self._run_async(_get)

    async def set(self, key: str, value: Any, *, ttl: float) -> None:
        def _set(cache: Cache):
            logger.debug("Storing"
            cache.set(key, value, expire=ttl)

        await self._run_async(_set)
