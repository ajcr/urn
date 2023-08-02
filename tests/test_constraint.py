from urn.constraint import ConstraintItem, union_constraint_disjuncts


def test_constraint_and():

    c1 = ConstraintItem("A")

    c1 &= ConstraintItem("A", max_=5)
    assert c1.min_ == 0
    assert c1.max_ == 5

    c1 &= ConstraintItem("A", min_=2, max_=7)
    assert c1.min_ == 2
    assert c1.max_ == 5

    c1 &= ConstraintItem("A", min_=6, max_=7)
    assert c1.min_ == 6
    assert c1.max_ == 5


def test_union_constraint_disjuncts():

    constraints = [
        [ConstraintItem("A", min_=2, max_=7)],
        [ConstraintItem("A", min_=3, max_=5)],
    ]

    union = list(union_constraint_disjuncts(constraints))

    assert union == [
        (1, {"A": ConstraintItem("A", min_=2, max_=7)}),
        (1, {"A": ConstraintItem("A", min_=3, max_=5)}),
        (2, {"A": ConstraintItem("A", min_=3, max_=5)}),
    ]
