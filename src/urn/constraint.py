import itertools
from collections.abc import Iterable, Sequence, Generator
from dataclasses import dataclass


INFINITY = float("inf")


@dataclass(eq=True)
class ConstraintItem:
    """Constraint on item.

    Bounds an integer range [min_, max_)
    """
    name: str
    min_: int = 0
    max_: int | float = INFINITY

    def __and__(self, other):
        if not isinstance(other, ConstraintItem):
            return NotImplemented

        if self.name != other.name:
            raise ValueError(f"{self.name} != {other.name}")

        return ConstraintItem(
            name=self.name,
            min_=max(self.min_, other.min_),
            max_=min(self.max_, other.max_),
        )


def reduce_constraints(
    constraints: Iterable[ConstraintItem]
) -> dict[str, ConstraintItem]:
    """Reduce collection of constraints by combining constraints
    on common items.
    """
    output = {}
    for constraint in constraints:
        if constraint.name in output:
            output[constraint.name] &= constraint
        else:
            output[constraint.name] = constraint
    return output


def union_constraint_disjuncts(
    seq: Sequence[Sequence[ConstraintItem]]
) -> Generator[tuple[int, dict[str, ConstraintItem]], None, None]:
    """Return the union of each subsequence of constraint disjuncts."""
    for n in range(1, len(seq) + 1):
        combs = itertools.combinations(seq, n)
        for cmb in combs:
            yield n, reduce_constraints(itertools.chain.from_iterable(cmb))