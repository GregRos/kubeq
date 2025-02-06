from kubeq.operators import *
from kubeq.selection.to_simplified_dnf import to_simplified_dnf


def start():
    lots = (
        Eq("1")
        .and_(Eq("3"), In("2", "4"))
        .or_(NotIn("5", "6"))
        .and_(NotRegex(".*"))
        .or_(NotGlob("*.py"))
    )
    lots = to_simplified_dnf(lots)

    print(visualize_operator(lots))
