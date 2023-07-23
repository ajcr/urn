
import pytest
from sympy import Poly
from sympy.abc import x

from qxy.evaluation import make_count_draw_polynomials
from qxy.constraint import ConstraintItem



@pytest.mark.parametrize(
    [
        "collection",
        "constraints",
        "selection_range",
        "expected_polynomials",
    ],
    [
        pytest.param(
            {"a": 5},
            {"a": ConstraintItem("a", min_=0)},
            range(0, 3),
            [Poly(10*x**2 + 5*x + 1, x)],
            id="5a, a>=0, selection 0..2",
        ),
        pytest.param(
            {"a": 5},
            {"a": ConstraintItem("a", min_=1)},
            range(0, 3),
            [Poly(10*x**2 + 5*x + 0, x)],
            id="5a, a>=1, selection 0..2",
        ),
        pytest.param(
            {"a": 4},
            {"a": ConstraintItem("a", min_=2)},
            range(0, 3),
            [Poly(6*x**2 + 0*x + 0, x)],
            id="4a, a>=2, selection 0..2",
        ),
        pytest.param(
            {"a": 4},
            {"a": ConstraintItem("a", min_=2)},
            range(0, 2),
            [Poly(0*x + 0, x)],
            id="4a, a>=2, selection 0..1",
        ),
        pytest.param(
            {"a": 2},
            {"a": ConstraintItem("a", min_=3)},
            range(0, 3),
            [Poly(0*x**2 + 0*x + 0, x)],
            id="2a, a>=3, selection 0..2",
        ),
        pytest.param(
            {"a": 2},
            {},
            range(0, 3),
            [Poly(x**2 + 2*x + 1, x)],
            id="2a, no constraint, selection 0..2",
        ),
        pytest.param(
            {"a": 2, "b": 5},
            {},
            range(0, 3),
            [Poly(x**2 + 2*x + 1, x), Poly(10*x**2 + 5*x + 1, x)],
            id="2a, 5b, no constraint, selection 0..2",
        ),
        pytest.param(
            {"a": 2, "b": 5},
            {"b": ConstraintItem("b", max_=2)},
            range(0, 4),
            [Poly(x**2 + 2*x + 1, x), Poly(5*x + 1, x)],
            id="2a, 5b, b<=1, selection 0..3",
        ),
    ],
)
def test_make_count_draw_polynomials(
    collection, constraints, selection_range, expected_polynomials
):    
    polys = make_count_draw_polynomials(
        collection, constraints, selection_range
    )
    assert polys == expected_polynomials


