from enum import Enum

ComputationType = Enum("ComputationType", ["COUNT", "PROBABILITY"])
ComputationAction = Enum("ComputationAction", ["DRAW"])
OutputFormat = Enum("OutputFormat", ["TABLE", "PLOT"])