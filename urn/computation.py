import itertools
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from urn.constraint import ConstraintItem
from urn.constants import ComputationAction, ComputationObject

class ComputationDescriptionError(Exception):
    pass


@dataclass
class ComputationDescription:
    """Description of a computation."""
    computation_type: ComputationAction = ComputationAction.COUNT
    object_type: ComputationObject = ComputationObject.DRAW
    selection_range: range | Sequence[int] | None = None
    collection: Mapping[str, int] | None = None
    constraints: Sequence[Sequence[ConstraintItem]] = ()
    with_replacement: bool = False
    is_finalised: bool = False

    def finalise(self) -> None:
        """Finalise computation so it can be evaluated.

        Check that computation is valid and modify attributes as required.
        """
        if self.collection is None:
            raise ComputationDescriptionError("Collection is undefined.")

        # No constraints: constrain all items by their count
        if not self.constraints:
            self.constraints = [
                [ConstraintItem(name, 0, count+1) for name, count in self.collection.items()]
            ]

        # If not using replacement and selection size is given, clip the selection size
        # upper bound to size of collection
        if not self.with_replacement and isinstance(self.selection_range, range):
            self.selection_range = range(
                self.selection_range.start,
                min(self.selection_range.stop, self.collection_size()+1),
            )

        # Error if a constraint applies to an item not in the collection
        c_names = {c.name for c in itertools.chain.from_iterable(self.constraints)}
        if self.collection and (missing := c_names - self.collection.keys()):
            raise ComputationDescriptionError(f"Constrained items not in collection: {missing}")

        self.is_finalised = True

    def selection_size_bounds(self) -> tuple[int, int]:
        if self.selection_range is None:
            return 0, self.collection_size()
        elif isinstance(self.selection_range, range):
            return self.selection_range.start, self.selection_range.stop
        else:
            return min(self.selection_range), max(self.selection_range) + 1

    def collection_size(self) -> int:
        if self.collection is None:
            raise ComputationDescriptionError("Collection is undefined.")
        return sum(self.collection.values())

    def x_label(self) -> str:
        return f"{self.object_type.name} size".lower()

    def y_label(self) -> str:
        return self.computation_type.name.lower()
