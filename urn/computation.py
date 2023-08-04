import itertools
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from typing import Literal

from urn.constraint import ConstraintItem, reduce_constraints


class ComputationDescriptionError(Exception):
    pass


@dataclass
class ComputationDescription:
    """Description of a computation."""
    computation_type: Literal["COUNT", "PROBABILITY"] = "COUNT"
    object_type: Literal["DRAW"] = "DRAW"
    selection_range: range | None = None
    collection: Mapping[str, int] | None = None
    constraints: Collection[Collection[ConstraintItem]] = None
    with_replacement: bool = False
    _is_finalised: bool = False

    def finalise(self) -> None:
        """Finalise computation so it can be evaluated.

        Check that computation is valid and modify attributes as required.
        """
        if self.collection is None:
            raise ComputationDescriptionError("Collection cannot be undefined.")

        # No constraints: constrain all items by their count
        if not self.constraints:
            self.constraints = [
                [ConstraintItem(name, 0, count+1) for name, count in self.collection.items()]
            ]

        # If not using replacement and selection size is given, clip the selection size
        # upper bound to size of collection
        if not self.with_replacement and self.selection_range is not None:
            self.selection_range = range(
                self.selection_range.start,
                min(self.selection_range.stop, self.collection_size()+1),
            )

        # Error if a constraint applies to an item not in the collection
        c_names = {c.name for c in itertools.chain.from_iterable(self.constraints)}
        if self.collection and (missing := c_names - self.collection.keys()):
            raise ComputationDescriptionError(f"Constrained items not in collection: {missing}")

        self._is_finalised = True

    def collection_size(self) -> int:
        return sum(self.collection.values())

    def x_label(self) -> str:
        return f"{self.object_type} size".lower()

    def y_label(self) -> str:
        return self.computation_type.lower()
