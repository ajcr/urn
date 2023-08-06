
import pytest
from sympy import Poly, Rational, binomial
from sympy.abc import x

from urn.evaluation import make_count_draw_polynomials, evaluate
from urn.constraint import ConstraintItem
from urn.computation import ComputationDescription
from urn.constants import ComputationAction, ComputationObject


@pytest.mark.parametrize(
    [
        "collection",
        "constraints",
        "selection_upper_bound",
        "expected_polynomials",
    ],
    [
        pytest.param(
            {"a": 5},
            {"a": ConstraintItem("a", min_=0)},
            3,
            [Poly(10*x**2 + 5*x + 1, x)],
            id="5a, a>=0, selection 0..2",
        ),
        pytest.param(
            {"a": 5},
            {"a": ConstraintItem("a", min_=1)},
            3,
            [Poly(10*x**2 + 5*x + 0, x)],
            id="5a, a>=1, selection 0..2",
        ),
        pytest.param(
            {"a": 4},
            {"a": ConstraintItem("a", min_=2)},
            3,
            [Poly(6*x**2 + 0*x + 0, x)],
            id="4a, a>=2, selection 0..2",
        ),
        pytest.param(
            {"a": 4},
            {"a": ConstraintItem("a", min_=2)},
            2,
            [Poly(0*x + 0, x)],
            id="4a, a>=2, selection 0..1",
        ),
        pytest.param(
            {"a": 2},
            {"a": ConstraintItem("a", min_=3)},
            3,
            [Poly(0*x**2 + 0*x + 0, x)],
            id="2a, a>=3, selection 0..2",
        ),
        pytest.param(
            {"a": 2},
            {},
            3,
            [Poly(x**2 + 2*x + 1, x)],
            id="2a, no constraint, selection 0..2",
        ),
        pytest.param(
            {"a": 2, "b": 5},
            {},
            3,
            [Poly(x**2 + 2*x + 1, x), Poly(10*x**2 + 5*x + 1, x)],
            id="2a, 5b, no constraint, selection 0..2",
        ),
        pytest.param(
            {"a": 2, "b": 5},
            {"b": ConstraintItem("b", max_=2)},
            4,
            [Poly(x**2 + 2*x + 1, x), Poly(5*x + 1, x)],
            id="2a, 5b, b<=1, selection 0..3",
        ),
    ],
)
def test_make_count_draw_polynomials(
    collection, constraints, selection_upper_bound, expected_polynomials
):    
    polys = make_count_draw_polynomials(
        collection, constraints, selection_upper_bound
    )
    assert polys == expected_polynomials


@pytest.mark.parametrize(
    ["computation", "expected_result"],
    [
        pytest.param(
            ComputationDescription(
                computation_type=ComputationAction.COUNT,
                object_type=ComputationObject.DRAW,
                selection_range=None,
                collection={"A": 5},
                constraints=[],
            ),
            [1, 5, 10, 10, 5, 1],
            id="Draw from 5A, no constraints",
        ),
        # The following can be verified by generating all combinations and counting
        # those that match the constraints, e.g.:
        #
        # >>> for draw_size in [3, 4, 5, 6, 7]: print(sum(
        # ...     1 for C in combinations(
        # ...         ["blue"]*12 + ["red"]*16 + ["green"]*11,
        # ...         draw_size,
        # ...     )
        # ...     if C.count("red") <= 3 or C.count("blue") == 3)
        # ... ))
        # 9139
        # ...
        # 11257389
        pytest.param(
            ComputationDescription(
                computation_type=ComputationAction.COUNT,
                object_type=ComputationObject.DRAW,
                selection_range=[3, 4, 5, 6, 7],
                collection={"blue": 12, "red": 16, "green": 11},
                constraints=[[ConstraintItem("red", 0, 4), ConstraintItem("blue", 3, 4)]],
            ),
            [220, 5940, 77220, 643500, 3460600],
            id="Count draws from RBG, one disjunct",
        ),
        pytest.param(
            ComputationDescription(
                computation_type=ComputationAction.COUNT,
                object_type=ComputationObject.DRAW,
                selection_range=[3, 4, 5, 6, 7],
                collection={"blue": 12, "red": 16, "green": 11},
                constraints=[[ConstraintItem("red", 0, 4)], [ConstraintItem("blue", 3, 4)]],
            ),
            [9139, 80431, 529529, 2693691, 11257389],
            id="Count draws from RBG, two disjuncts",
        ),
        pytest.param(
            ComputationDescription(
                computation_type=ComputationAction.COUNT,
                object_type=ComputationObject.DRAW,
                selection_range=[5, 6, 7],
                collection={"blue": 12, "red": 16, "green": 11},
                constraints=[
                    [ConstraintItem("red", 0, 4), ConstraintItem("green", 2, 5)],
                    [ConstraintItem("blue", 3, 4)],
                    [ConstraintItem("green", 5, 12)],
                ],
            ),
            [317372, 2118303, 10066617],
            id="Count draws from RBG, three disjuncts",
        ),
        pytest.param(
            ComputationDescription(
                computation_type=ComputationAction.PROBABILITY,
                object_type=ComputationObject.DRAW,
                selection_range=[3, 4, 5, 6, 7],
                collection={"blue": 12, "red": 16, "green": 11},
                constraints=[[ConstraintItem("red", 0, 4)], [ConstraintItem("blue", 3, 4)]],
            ),
            [
                Rational(9139, binomial(39, 3)),
                Rational(80431, binomial(39, 4)),
                Rational(529529, binomial(39, 5)),
                Rational(2693691, binomial(39, 6)),
                Rational(11257389, binomial(39, 7)),
            ],
            id="Probability draw from RBG, two disjuncts",
        ),
    ]
)
def test_evaluate(computation, expected_result):
    computation.finalise()
    assert evaluate(computation) == expected_result
