from itertools import product
from kubeq.query._reductions._to_dnf import assert_dnf
from kubeq.query._selection._selection_formula import SelectionFormula
import kubeq.query._operators as oprs
import kubeq.query._attr as attr


def separate_formula(dnf_formula: SelectionFormula) -> list[SelectionFormula]:
    all_formulas: list[SelectionFormula] = []
    clauses: list[tuple[attr.Any, list[oprs.Op]]] = []
    for key, op in dnf_formula:
        match op:
            case oprs.Or():
                clauses.append((key, op.operands))
            case oprs.Always():
                continue
            case oprs.Never():
                raise Exception(f"Clause on {key} can match no resources!")
    if not clauses:
        raise Exception("Clauses would match all resources!")

    prod = product(*[ops for _, ops in clauses])
    for part_formula in prod:
        formula_dict = {}
        for i, op in enumerate(part_formula):
            key, _ = clauses[i]
            formula_dict[key] = op
        all_formulas.append(SelectionFormula(formula_dict))
    return all_formulas
