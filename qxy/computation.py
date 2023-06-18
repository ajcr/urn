import itertools
from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import Literal

from qxy.constraint import ConstraintItem


@dataclass
class Computation:
    """Description of a computation."""
    computation_type: Literal["COUNT", "PROBABILITY"]
    object_type: Literal["DRAW", "SEQUENCE"]
    selection_range: range
    collection: Mapping[str, int]
    constraints: Collection[Collection[ConstraintItem]] = None
    with_replacement: bool = False

    def __post_init__(self) -> None:

        # No constraints: constrain all items by their count
        if not self.constraints:
            self.constraints = [
                [ConstraintItem(name, 0, count+1) for name, count in self.collection.items()]
            ]

        # If not using replacement, clip selection size upper bound to size of collection
        if not self.with_replacement:
            self.selection_range = range(
                self.selection_range.start,
                min(self.selection_range.stop, self.collection_size()+1),
            )

        # Error if a constraint applies to an item not in the collection
        c_names = {c.name for c in itertools.chain.from_iterable(self.constraints)}
        if missing := c_names - self.collection.keys():
            raise ValueError(f"Constrained items not in collection: {missing}")

    def collection_size(self) -> int:
        return sum(self.collection.values())

    def x_label(self) -> str:
        return f"{self.object_type} size".lower()

    def y_label(self) -> str:
        return self.computation_type.lower()