import itertools
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from urn.constraint import ConstraintItem
from urn.constants import ComputationAction, ComputationObject

class ComputationDescriptionError(Exception):
    pass


@dataclass(eq=True)
class ComputationDescription:

    computation_type: ComputationAction = ComputationAction.COUNT
    object_type: ComputationObject = ComputationObject.DRAW
    selection_range: range | Sequence[int] | None = None
    collection: Mapping[str, int] = field(default_factory=dict)
    constraints: Sequence[Sequence[ConstraintItem]] = field(default_factory=list)
    with_replacement: bool = False
    is_finalised: bool = False

    def finalise(self) -> None:
        """Finalise computation so it can be evaluated.

        Check that computation is valid and modify attributes as required.
        """
        # No constraints: constrain items by count if drawing without replacement
        if not self.constraints and not self.with_replacement:
            self.constraints = [
                [
                    ConstraintItem(name, 0, count+1)
                    for name, count in self.collection.items()
                ]
            ]

        # If selection size is given, clip upper bound to size of collection
        if not self.with_replacement and isinstance(self.selection_range, range):
            self.selection_range = range(
                self.selection_range.start,
                min(self.selection_range.stop, self.collection_size()+1),
            )
        elif not self.with_replacement and isinstance(self.selection_range, Sequence):
            self.selection_range = [
                n for n in self.selection_range if n <= self.collection_size()
            ]

        if self.with_replacement and self.selection_range is None:
            raise ComputationDescriptionError(
                "Must specify selection number if drawing with replacement."
            )

        # Error if a constraint applies to an item not in the collection
        c_names = {c.name for c in itertools.chain.from_iterable(self.constraints)}
        if self.collection and (missing := c_names - self.collection.keys()):
            raise ComputationDescriptionError(
                f"Constrained items not in collection: {missing}"
            )

        self.is_finalised = True

    def selection_size_bounds(self) -> tuple[int, int]:
        if self.selection_range is None:
            return 0, self.collection_size() + 1
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
