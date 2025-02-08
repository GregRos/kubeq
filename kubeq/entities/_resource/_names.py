from dataclasses import dataclass

from box import Box


@dataclass
class KubeNames:
    main: str
    plural: str
    short: tuple[str, ...]

    @staticmethod
    def parse_resource(resource: Box):
        return KubeNames(
            main=resource.singularResource,
            plural=resource.name,
            short=tuple(resource.shortNames),
        )
