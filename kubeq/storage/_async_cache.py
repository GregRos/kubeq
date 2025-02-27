from asyncio import EventLoop, get_event_loop
from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Any, Awaitable, Callable, Unpack
from diskcache import Cache
from httpx import Response

from kubeq.logging import sources
from kubeq.storage._info import CacheInfo
from kubeq.storage._features import CacheFeatures
from kubeq.storage._entry import CacheEntry
from kubeq.utils._custom_dunder import dunder_invoker

logger = sources.cache.logger


class AsyncCache:
    _thread_pool = ThreadPoolExecutor(max_workers=4)

    def __init__(self, cache: Cache):
        self._cache = cache

    async def _run_async[R](self, func: Callable[[Cache], R]) -> R:
        def _run():
            return func(self._cache)

        return await get_event_loop().run_in_executor(self._thread_pool, _run)

    def _get_info(self, key: object) -> CacheInfo | None:
        info = CacheInfo.from_(key)
        if not info:
            logger.debug(f"MISSING INFO: {str(key)}")
            return None
        return info

    def _get_entry(self, key: object) -> CacheEntry | None:
        info = self._get_info(key)
        if not info:
            return None

    async def delete(self, key: object) -> bool:
        info = self._get_info(key)
        if not info:
            return False

        logger.debug(f"DELETING: {str(info)}")

        def _delete(cache: Cache):
            cache.pop(info.key, None)

        await self._run_async(_delete)
        return True

    async def get(self, key: object) -> Any | None:
        info = self._get_info(key)
        if not info:
            return None
        if info.features.get("cache_force", False):
            logger.debug(f"CACHE FORCED: {str(info)}")
            await self.delete(key)
            return None

        def _get(cache: Cache):
            entry: CacheEntry | None = cache.get(info.key)  # type: ignore
            if entry:
                logger.debug(
                    f"Serving from cache",
                    {
                        "key": str(info.key),
                        "value": str(entry.value),
                    },
                )
                return entry.value
            else:
                logger.debug(
                    f"Cache miss",
                    {
                        "key": str(info.key),
                    },
                )
                return None

        return await self._run_async(_get)

    async def store(
        self,
        key: object,
        value: Any,
        /,
        **features: Unpack[CacheFeatures],
    ) -> bool:
        entry = CacheEntry.from_(key, value, **features)
        if not entry:
            return False
        if entry.features.get("no_cache", False):
            return False

        def _set(cache: Cache):

            cache.set(
                entry.key,
                entry,
                expire=features.get("ttl", None),
            )
            logger.debug(
                f"STORED: {entry.info}",
                {
                    "value": str(entry.value),
                },
            )

        await self._run_async(_set)
        return True
