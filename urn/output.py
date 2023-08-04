from collections.abc import Sequence
from dataclasses import dataclass
from sympy import Rational
from typing import Literal

import tabulate
import uniplot

from urn.computation import ComputationDescription


@dataclass
class Output:
    """Output config."""

    output_fmt: Literal["TABLE", "PLOT"] = "TABLE"
    output_float: bool = False

    def output(self, computation: ComputationDescription, evaluation: Sequence[Rational]) -> str:
        """Create output."""
        if self.output_fmt == "PLOT":
            return self.make_plot(computation, evaluation)
        else:
            return self.make_table(computation, evaluation)

    def make_table(self, computation: ComputationDescription, evaluation: Sequence[Rational]) -> str:
        str_func = "{:.15f}".format if self.output_float else str
        rows = list(
            zip(
                computation.selection_range,
                map(str_func, evaluation),
                strict=True,
            )
        )
        headers= [computation.x_label(), computation.y_label()]
        return tabulate.tabulate(rows, headers=headers)
    
    def make_plot(self, computation: ComputationDescription, evaluation: Sequence[Rational]) -> str:
        if len(computation.selection_range) != len(evaluation):
            raise ValueError(
                "Evaluation sequence must be same length as computation.selection_range."
            )
        plt = uniplot.plot_to_string(
            ys=evaluation,
            xs=computation.selection_range,
            color=True,
            y_min=0,
        )
        return "\n".join(plt)
