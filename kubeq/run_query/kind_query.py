from kubeq.entities._db import KubeResourceDB
from kubeq.query._selection._selection_formula import SelectionFormula


def run_kind_query(kind_db: KubeResourceDB, kind_query: SelectionFormula):
    for r in kind_db:
        if kind_query(r):
            yield r
