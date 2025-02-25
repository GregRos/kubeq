from kubeq.query._utils.render_op import render_operator
from kubeq.query._operators import *
from kubeq.query import *


def start():
    oprs._boolean.And()
    r = (
        Eq("1")
        .and_(Eq("3"), In("2", "4"))
        .or_(NotIn("5", "6"))
        .and_(NotRegex(".*"))
        .or_(NotGlob("*.py"))
        .and_(Eq("7").or_(Eq("1"), Eq("5"), Eq("10")))
    )
    dnf = red.Minimizing_Dnf()
    r = dnf.reduce(r)

    print(render_operator(r))
    print(repr(r))


start()
