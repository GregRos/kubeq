from logging import Logger

from . import _base_source

api_client = _base_source.LogSource("kubeq.http_client", "🌍")
cache = _base_source.LogSource("kubeq.cache", "🗃️ ")
simplifier = _base_source.LogSource("kubeq.simplifier", "🗜️")
cli = _base_source.LogSource("kubeq.cli", "🖥️")

cli.logger.debug("Logging initialized")
del _base_source
