from kubeq.operators import *


def start():
    lots = (
        Eq("1")
        .and_(Eq("3"), In("2", "4"))
        .or_(NotIn("5", "6"))
        .and_(NotRegex(".*"))
        .or_(NotGlob("*.py"))
    )

    print(visualize_operator(lots))
