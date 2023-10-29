import lark
import pytest

from urn.constraint import ConstraintItem, INFINITY
from urn.computation import ComputationDescription
from urn.constants import ComputationType, ComputationAction
from urn.parsing import BuildComputation


@pytest.fixture(scope="session")
def parser(request):
    rel_to = request.config.rootdir.join("urn").join("urn")
    return lark.Lark.open("grammar.lark", rel_to=str(rel_to))


@pytest.mark.parametrize(
    ["query", "expected_computation"],
    [
        pytest.param(
            "COUNT DRAWS FROM A=7;",
            ComputationDescription(
                computation_type=ComputationType.COUNT,
                computation_action=ComputationAction.DRAW,
                selection_range=None,
                collection={"A": 7},
                constraints=[],
            ),
            id="Count draw, no constraints",
        ),
        pytest.param(
            "COUNT DRAWS FROM A=7 WHERE A<=5;",
            ComputationDescription(
                computation_type=ComputationType.COUNT,
                computation_action=ComputationAction.DRAW,
                selection_range=None,
                collection={"A": 7},
                constraints=[[ConstraintItem("A", 0, 6)]],
            ),
            id="Count draw, one constraints",
        ),
        pytest.param(
            "COUNT DRAWS FROM A=7 WHERE A<=5 AND A > 3;",
            ComputationDescription(
                computation_type=ComputationType.COUNT,
                computation_action=ComputationAction.DRAW,
                selection_range=None,
                collection={"A": 7},
                constraints=[
                    [ConstraintItem("A", 0, 6), ConstraintItem("A", 4, INFINITY)]
                ],
            ),
            id="Count draw, two constraints on same item",
        ),
        pytest.param(
            "COUNT DRAWS FROM A=7 WHERE 4 < A <= 5;",
            ComputationDescription(
                computation_type=ComputationType.COUNT,
                computation_action=ComputationAction.DRAW,
                selection_range=None,
                collection={"A": 7},
                constraints=[[ConstraintItem("A", 5, 6)]],
            ),
            id="Count draw, chained constraint",
        ),
        pytest.param(
            "COUNT DRAWS FROM A=7 WHERE A > 4, A <= 5;",
            ComputationDescription(
                computation_type=ComputationType.COUNT,
                computation_action=ComputationAction.DRAW,
                selection_range=None,
                collection={"A": 7},
                constraints=[
                    [ConstraintItem("A", 5, INFINITY), ConstraintItem("A", 0, 6)]
                ],
            ),
            id="Count draw, repeated AND constraint using ','",
        ),
        pytest.param(
            "COUNT DRAWS FROM A=7, B=11 WHERE A = 2 OR B <= 7;",
            ComputationDescription(
                computation_type=ComputationType.COUNT,
                computation_action=ComputationAction.DRAW,
                selection_range=None,
                collection={"A": 7, "B": 11},
                constraints=[[ConstraintItem("A", 2, 3)], [ConstraintItem("B", 0, 8)]],
            ),
            id="Count draw, two constraint disjuncts",
        ),
        pytest.param(
            "COUNT DRAWS 2..8 FROM A=7, B=9;",
            ComputationDescription(
                computation_type=ComputationType.COUNT,
                computation_action=ComputationAction.DRAW,
                selection_range=range(2, 9),
                collection={"A": 7, "B": 9},
                constraints=[],
            ),
            id="Count draw, selection range, no constraints",
        ),
    ],
)
def test_build_computation_description_from_string(parser, query, expected_computation):
    tree = parser.parse(query)
    comp = BuildComputation().transform(tree)
    assert comp.computation == expected_computation
