import functools
from pathlib import Path

from diskcache import Cache

from kubeq.storage._async_cache import AsyncCache


class _KubeqStorageController:
    @functools.cached_property
    def _cache_dir(self):
        return self._root_path / "cache"

    def __init__(self, root_path: Path):
        self._root_path = root_path
        self._root_path.mkdir(exist_ok=True, parents=True)

    @functools.cached_property
    def cache(self):
        c = Cache(directory=str(self._cache_dir))
        return AsyncCache(c)


Storage = _KubeqStorageController(Path.home() / ".kubeq")
