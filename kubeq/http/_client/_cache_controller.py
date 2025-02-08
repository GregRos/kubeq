from pathlib import Path
from diskcache import Cache


class CachingController:
    @staticmethod
    def setup_cache_dir():
        dir = Path.home() / ".kubeq"
        dir.mkdir(exist_ok=True)
        return dir
