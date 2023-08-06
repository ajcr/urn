from collections.abc import Collection, Mapping

import lark
from sympy import Poly, Rational, binomial, prod
from sympy.abc import x

from urn.computation import ComputationDescription, ComputationDescriptionError
from urn.constraint import ConstraintItem, union_constraint_disjuncts
from urn.parsing import BuildComputation
from urn.constants import ComputationAction, ComputationObject


def make_count_draw_polynomials(
    collection: Mapping[str, int],
    constraints: Mapping[str, ConstraintItem],
    selection_upper_bound: int,
) -> list[Poly]:
    """Construct a polynomial for each item in the collection."""
    polys = []
    for item, item_count in collection.items():
        if item in constraints:
            min_ = constraints[item].min_
            max_ = min([item_count+1, selection_upper_bound, constraints[item].max_])
        else:
            min_ = 0
            max_ = min([item_count+1, selection_upper_bound])
        polys.append(
            degrees_to_polynomial_with_binomial_coeff(
                range(min_, max_), item_count  # type: ignore
            )
        )
    return polys


def evaluate(computation: ComputationDescription) -> list[Rational | int]:
    """Evaluate the computation described by the object."""
    if not computation.is_finalised or computation.collection is None:
        raise ComputationDescriptionError(
            "Computation must be finalised before evaluation (use `finalise` method)"
        )

    _, selection_upper_bound = computation.selection_size_bounds()

    if computation.object_type == ComputationObject.DRAW:

        poly = Poly(0, x)

        for n, constraints in union_constraint_disjuncts(computation.constraints):
            # Inclusion/Exclusion
            poly += (-1)**(n+1) * prod(
                    make_count_draw_polynomials(
                    collection=computation.collection,
                    constraints=constraints,
                    selection_upper_bound=selection_upper_bound,
                )
            )
        if computation.selection_range is not None:
            counts = [poly.coeff_monomial(x**y) for y in computation.selection_range]
        else:
            # Find implied selection sizes (monomials with non-zero coeffs)
            pairs = [(power, coeff) for (power,), coeff in poly.as_dict().items()]
            selection_range, counts = zip(*pairs)
            computation.selection_range = selection_range

    else:
        raise NotImplementedError(computation.object_type)

    if computation.computation_type == ComputationAction.COUNT:
        return list(counts)  # type: ignore

    if computation.computation_type == ComputationAction.PROBABILITY:
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
