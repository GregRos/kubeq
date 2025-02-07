from kubeq.query._utils.render_op import render_operator
from kubeq.query._operators import *
from kubeq.query import *


def start():
    oprs._boolean.And()
    lots = (
        Eq("1")
        .and_(Eq("3"), In("2", "4"))
        .or_(NotIn("5", "6"))
        .and_(NotRegex(".*"))
        .or_(NotGlob("*.py"))
        .and_(Eq("7").or_(Eq("1"), Eq("5"), Eq("10")))
    )
    lots = red.to_minimal_dnf(lots)

    print(render_operator(lots))
