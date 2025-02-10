import functools
from typing import Iterable
from rich import print, box
from rich.table import Table, Column

from kubeq.entities._resource._resource import KubeResource
from kubeq.entities._resource._sub_resource import KubeSubResource
from ._verbs import verbs


class Print_RDB:
    def __init__(self, input: Iterable[KubeResource]):
        self.input = [*input]

    @functools.cached_property
    def columns(self):
        yield Column(
            header="SH",
            footer="SH",
            max_width=4,
            justify="center",
        )
        yield Column(
            header="KIND",
            footer="KIND",
        )
        yield Column(
            header="VERSION",
            footer="VERSION",
        )
        for verb in verbs.values():
            yield Column(
                header=verb.short,
                footer=verb.short,
                justify="center",
                width=2,
                no_wrap=True,
            )

    def _resource_row(self, resource: KubeResource):
        match resource.names.short:  # SH
            case []:
                yield ""
            case [x, *_]:
                yield x

        yield resource.ident  # KIND
        for verb in verbs.values():
            yield verb.short if verb.name in resource.verbs else ""  # VERBS
        yield resource.kind.parent  # VERSION

    def _subresource_row(self, sub: KubeSubResource):
        yield ""  # SH
        yield f"  ⤷ {sub.name}"  # KIND
        for verb in verbs.values():
            yield verb.short if verb.name in sub.verbs else ""  # VERBS
        yield sub.kind.parent  # VERSION

    def render(self):
        table = Table(
            title="Known Resources",
            caption_justify="center",
            padding=(0, 1),
            box=None,
            border_style="bright_black",
        )
        table.columns.extend(self.columns)
        for resource in self.input:
            table.add_row(*self._resource_row(resource))
            for sub in resource.kids.values():
                table.add_row(*self._subresource_row(sub))

        return table
