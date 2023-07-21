
import pytest
from sympy import Poly
from sympy.abc import x

from qxy.evaluation import make_count_draw_polynomials
from qxy.constraint import ConstraintItem



@pytest.mark.parametrize(
    ["collection", "constraints", "selection_range", "expected"],
    [
        pytest.param(
            {"a": 5},
            {"a": ConstraintItem("a", 3)},
            range(0, 3),
            # [poly]
        )
    ],
)
def test_make_count_draw_polynomials(
    collection, constraints, selection_range, expected
):    
    polys = make_count_draw_polynomials(
        collection, constraints, selection_range
    )
    assert polys == expected


