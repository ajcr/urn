from collections.abc import Collection, Mapping

import lark
from sympy import Poly, Rational, binomial, prod, factorial
from sympy.abc import x

from urn.computation import ComputationDescription, ComputationDescriptionError
from urn.constraint import ConstraintItem, union_constraint_disjuncts
from urn.parsing import BuildComputation
from urn.constants import ComputationType, ComputationAction


def make_count_draw_polynomials(
    collection: Mapping[str, int],
    constraints: Mapping[str, ConstraintItem],
    selection_upper_bound: int,
) -> list[Poly]:
    polys = []
    for item, item_count in collection.items():
        if item in constraints:
            min_ = constraints[item].min_
            max_ = min([item_count + 1, selection_upper_bound, constraints[item].max_])
        else:
            min_ = 0
            max_ = min([item_count + 1, selection_upper_bound])
        polys.append(
            degrees_to_polynomial_with_binomial_coeff(
                range(min_, max_), item_count  # type: ignore
            )
        )
    return polys


def make_count_draw_with_replacement_polynomials(
    computation: ComputationDescription,
    constraints: Mapping[str, ConstraintItem],
) -> list[Poly]:
    polys = []
    _, selection_upper_bound = computation.selection_size_bounds()
    for item, item_count in computation.collection.items():
        if item in constraints:
            min_ = constraints[item].min_
            max_ = min(constraints[item].max_, selection_upper_bound)
        else:
            min_ = 0
            max_ = selection_upper_bound
        polys.append(
            degrees_to_polynomial_with_fractional_coeff(
                range(min_, max_),  # type: ignore
                item_count,
            )
        )
    return polys


def evaluate(computation: ComputationDescription) -> list[Rational | int]:
    """Evaluate the computation described by the object."""
    if not computation.is_finalised or computation.collection is None:
        raise ComputationDescriptionError(
            "Computation must be finalised before evaluation (use `finalise` method)"
        )

    if (
        computation.computation_action == ComputationAction.DRAW
        and computation.with_replacement is False
    ):
        _, selection_upper_bound = computation.selection_size_bounds()
        poly = Poly(0, x)
        for n, constraints in union_constraint_disjuncts(computation.constraints):
            poly += (-1) ** (n + 1) * prod(
                make_count_draw_polynomials(
                    collection=computation.collection,
                    constraints=constraints,
                    selection_upper_bound=selection_upper_bound,
                )
            )
        if computation.selection_range is not None:
            counts = [poly.coeff_monomial(x ** y) for y in computation.selection_range]
        else:
            # Find implied selection sizes (monomials with non-zero coeffs)
            pairs = [(power, coeff) for (power,), coeff in poly.as_dict().items()]
            selection_range, counts = zip(*pairs)
            computation.selection_range = selection_range

        if computation.computation_type == ComputationType.COUNT:
            return list(counts)  # type: ignore

        if computation.computation_type == ComputationType.PROBABILITY:
            total_items = computation.collection_size()
            possibilities = [
                binomial(total_items, y) for y in computation.selection_range
            ]
            return [c / p for c, p in zip(counts, possibilities, strict=True)]

    elif (
        computation.computation_action == ComputationAction.DRAW
        and computation.with_replacement is True
    ):
        assert computation.selection_range is not None

        size = computation.collection_size()
        total_unconstrained_draws = [size ** n for n in computation.selection_range]

        if computation.computation_type == ComputationType.COUNT:
            if not computation.constraints:
                return total_unconstrained_draws

        poly = Poly(0, x)
        for n, constraints in union_constraint_disjuncts(computation.constraints):
            poly += (-1) ** (n + 1) * prod(
                make_count_draw_with_replacement_polynomials(
                    computation=computation,
                    constraints=constraints,
                )
            )

        coeffs = [poly.coeff_monomial(x ** y) for y in computation.selection_range]
        factorials = [factorial(n) for n in computation.selection_range]
        counts = [c * f for c, f in zip(coeffs, factorials, strict=True)]

        if computation.computation_type == ComputationType.COUNT:
            return counts

        if computation.computation_type == ComputationType.PROBABILITY:
            return [
                count / total
                for count, total in zip(counts, total_unconstrained_draws, strict=True)
            ]

    else:
        raise NotImplementedError(computation.computation_action)

    raise NotImplementedError(computation.computation_type)


def degrees_to_polynomial_with_binomial_coeff(degrees: Collection[int], n: int) -> Poly:
    """For each degree `d`, create the polynomial with terms
    of degree `d` having binomial coefficient `bin(n, d)`:

        {0, 2, 5} -> bin(n, 5)*x**5 + bin(n, 2)*x**2 + 1

    """
    coeffs = {degree: binomial(n, degree) for degree in degrees}
    return Poly.from_dict(coeffs, x)


def degrees_to_polynomial_with_fractional_coeff(
    degrees: Collection[int], n: int
) -> Poly:
    """
    For each degree `d`, create the polynomial with those
    terms with coefficient (n**d / d!) where n is the count
    of the item in the collection:

        {5} -> (n**5 / 5!) * x**5

    """
    coeffs = {degree: Rational(n ** degree, factorial(degree)) for degree in degrees}
    return Poly.from_dict(coeffs, x)


def process_query(parser: lark.Lark, query: str) -> str:
    """Parse query, build computation, evaulate and return result."""
    tree = parser.parse(query)
    builder = BuildComputation()
    build: BuildComputation = builder.transform(tree)
    build.computation.finalise()
    evaluation = evaluate(build.computation)
    return build.output.output(build.computation, evaluation)
