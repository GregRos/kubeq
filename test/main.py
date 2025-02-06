from kubeq.query.operators import *


def start():
    lots = (
        Eq("1")
        .and_(Eq("3"), In("2", "4"))
        .or_(NotIn("5", "6"))
        .and_(NotRegex(".*"))
        .or_(NotGlob("*.py"))
        .and_(Eq("7").or_(Eq("1"), Eq("5"), Eq("10")))
    )
    lots = to_minimal_dnf(lots)

    print(visualize_operator(lots))
