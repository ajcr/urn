from typing import Collection

import lark
from sympy import Poly, Rational, binomial, prod
from sympy.abc import x

from urn.computation import ComputationDescription, ComputationDescriptionError
from urn.constraint import ConstraintItem, union_constraint_disjuncts
from urn.output import Output
from urn.parsing import BuildComputation


def make_count_draw_polynomials(
    collection: dict[str, int],
    constraints: dict[str, ConstraintItem],
    selection_range: range,
) -> list[Poly]:
    """Construct a polynomial for each item in the collection."""
    polys = []
    for item, item_count in collection.items():
        if item in constraints:
            min_ = constraints[item].min_
            max_ = min([item_count+1, selection_range.stop, constraints[item].max_])
        else:
            min_ = 0
            max_ = min([item_count+1, selection_range.stop])
        polys.append(
            degrees_to_polynomial_with_binomial_coeff(range(min_, max_), item_count)
        )
    return polys


def evaluate(computation: ComputationDescription) -> list[Rational]:
    """Evaluate the computation described by the object."""
    if not computation._is_finalised:
        raise ComputationDescriptionError(
            "Computation must be finalised before evaluation (use `finalise` method)"
        )

    if computation.object_type == "DRAW":

        p = 0
        for n, constraints in union_constraint_disjuncts(computation.constraints):
            # Inclusion/Exclusion
            p += (-1)**(n+1) * prod(
                    make_count_draw_polynomials(
                    collection=computation.collection,
                    constraints=constraints,
                    selection_range=computation.selection_range,
                )
            )
        counts = [p.coeff_monomial(x**y) for y in computation.selection_range]

    else:
        raise NotImplementedError(computation.object_type)

    if computation.computation_type == "COUNT":
        return counts

    if computation.computation_type == "PROBABILITY":
        total_items = computation.collection_size()
        possibilities = [binomial(total_items, y) for y in computation.selection_range]
        return [c/p for c, p in zip(counts, possibilities, strict=True)]

    raise NotImplementedError(computation.computation_type)


def degrees_to_polynomial_with_binomial_coeff(degrees: Collection[int], n: int) -> Poly:
    """For each degree `d` in a set, create the polynomial with terms
    of degree `d` having binomial coefficient `bin(n, d)`:

        {0, 2, 5} -> bin(n, 5)*x**5 + bin(n, 2)*x**2 + 1

    """
    degree_coeff_dict = {}

    for degree in degrees:
        degree_coeff_dict[degree] = binomial(n, degree)

    return Poly.from_dict(degree_coeff_dict, x)


def process_query(parser: lark.Lark, query: str) -> str:
    """Parse query, build computation, evaulate and return result."""
    tree = parser.parse(query)
    builder = BuildComputation()
    build: BuildComputation = builder.transform(tree)
    build.computation.finalise()
    evaluation = evaluate(build.computation)
    return build.output.output(build.computation, evaluation)
