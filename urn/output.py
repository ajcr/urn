from collections.abc import Sequence
from dataclasses import dataclass
from sympy import Rational

import tabulate
import uniplot

from urn.computation import ComputationDescription
from urn.constants import OutputFormat


@dataclass
class Output:
    """Output config."""

    output_fmt: OutputFormat = OutputFormat.TABLE
    output_float: bool = False

    def output(
        self,
        computation: ComputationDescription,
        evaluation: Sequence[Rational | int]
    ) -> str:
        """Create output."""
        if self.output_fmt == OutputFormat.PLOT:
            return self.make_plot(computation, evaluation)
        else:
            return self.make_table(computation, evaluation)

    def make_table(
        self,
        computation: ComputationDescription,
        evaluation: Sequence[Rational | int],
    ) -> str:
        if computation.selection_range is None:
            raise TypeError("selection range is None")
        if self.output_float:
            values = map(float, evaluation)
        else:
            values = evaluation
        rows = list(
            zip(
                computation.selection_range,
                map(str, values),
                strict=True,
            )
        )
        headers= [computation.x_label(), computation.y_label()]
        return tabulate.tabulate(rows, headers=headers)
    
    def make_plot(
        self,
        computation: ComputationDescription,
        evaluation: Sequence[Rational | int],
    ) -> str:
        if computation.selection_range is None:
            raise TypeError("selection range is None")
        if len(computation.selection_range) != len(evaluation):
            raise ValueError(
                "Evaluation sequence must be same length as selection range."
            )
        plt = uniplot.plot_to_string(
            ys=evaluation,
            xs=computation.selection_range,
            color=True,
            y_min=0,
        )
        return "\n".join(plt)
