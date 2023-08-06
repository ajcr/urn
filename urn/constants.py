from enum import Enum

ComputationAction = Enum("ComputationType", ["COUNT", "PROBABILITY"])
ComputationObject = Enum("ComputationAction", ["DRAW"])
OutputFormat = Enum("OutputFormat", ["TABLE", "PLOT"])