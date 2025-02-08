import functools
from pathlib import Path

from diskcache import Cache


class _KubeqStorageController:
    @functools.cached_property
    def _cache_dir(self):
        return self._root_path / "cache"

    def __init__(self, root_path: Path):
        self._root_path = root_path
        self._root_path.mkdir(exist_ok=True, parents=True)

    @functools.cached_property
    def cache(self):
        return Cache(directory=str(self._cache_dir))


Storage = _KubeqStorageController(Path.home() / ".kubeq")
