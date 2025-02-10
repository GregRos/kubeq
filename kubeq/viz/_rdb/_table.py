import functools
from typing import Iterable
from rich import print, box
from rich.table import Table, Column

from kubeq.entities._resource._resource import KubeResource
from kubeq.entities._resource._sub_resource import KubeSubResource
from kubeq.entities._resource._verbs import KubeVerb
from ._verbs import all_verbs


class Table_RDB:
    def __init__(
        self, input: Iterable[KubeResource], /, subresource_rows: bool = False
    ):
        self.input = [*input]
        self.subresource_rows = subresource_rows

    @classmethod
    @functools.cache
    def columns(cls):
        yield Column(header="SH", footer="SH", max_width=4, justify="center")
        yield Column(
            header="KIND",
            footer="KIND",
        )
        for verb in all_verbs.values():
            yield Column(
                header=verb.short,
                footer=verb.short,
                justify="center",
                width=2,
                no_wrap=True,
            )
        yield Column(header="VERSION", footer="VERSION")

    @classmethod
    def _get_verbs_row(cls, verb_list: Iterable[KubeVerb]):
        verb_set = set(verb_list)
        for verb_name, verb_repr in all_verbs.items():
            yield verb_repr.emoji if verb_name in verb_set else ""

    @classmethod
    def _resource_row(cls, resource: KubeResource):
        match resource.names.short:  # SH
            case []:
                yield ""
            case [x, *_]:
                yield x

        yield resource.ident  # KIND
        yield from cls._get_verbs_row(resource.verbs)
        yield resource.kind.parent  # VERSION

    @classmethod
    def _subresource_row(cls, sub: KubeSubResource):
        yield ""  # SH
        yield f"  ⤷ {sub.name}"  # KIND
        yield from cls._get_verbs_row(sub.verbs)  # VERBS
        yield sub.kind.parent  # VERSION

    def __rich__(self):
        table = Table(
            title="Known Resources",
            caption_justify="center",
            padding=(0, 1),
            box=None,
            border_style="bright_black",
            footer_style="bright_black",
        )
        table.columns.extend(self.columns())
        for resource in self.input:
            table.add_row(*self._resource_row(resource))
            if self.subresource_rows:
                for sub in resource.kids.values():
                    table.add_row(*self._subresource_row(sub))

        return table
