from typing import Iterable

from reactivex import just
from kubeq.entities._db import KubeResourceDB
from rich import print
from rich.table import Table, Column

from kubeq.entities._resource._resource import KubeResource
from ._viz_console import console
from kubeq.entities._resource._verbs import KubeVerb, KubeVerbTuple


def _verbs_to_str(verbs: Iterable[KubeVerb]) -> str:
    return " ".join(_verb_to_short[x] for x in verbs)


def print_rdb(rdb: KubeResourceDB):
    table = Table(
        title="Known Resources",
        caption_justify="center",
        padding=(0, 1),
        box=None,
        border_style="bright_black",
    )

    table.add_column("SH", max_width=3)
    table.add_column("KIND")
    for l, _ in _verbs_in_order.values():
        table.add_column(l, justify="center", width=2, no_wrap=True)
    table.add_column("VERSION")
    ordered = sorted(rdb, key=lambda x: (x.kind.name, x.kind.group, x.kind.version))
    for x in ordered:
        kids_has_status = any(y.is_status for y in x.kids.values())

        vees = [
            tick if name in x.verbs else ""
            for name, (_, tick) in _verbs_in_order.items()
        ]
        scope_mark = "ⁿˢ" if x.is_namespaced else ""

        name_col = f"{x.kind.name}{scope_mark}"
        first_short = x.names.short[0] if x.names.short else ""
        table.add_row(first_short, f"{name_col}", *vees, x.kind.parent)
        for y in x.kids.values():
            vees = [
                tick if name in y.verbs else ""
                for name, (_, tick) in _verbs_in_order.items()
            ]
            table.add_row("", f" ⤷ {y.ident}", *vees, y.kind.parent)
    console.print(table)
