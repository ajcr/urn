import lark

from urn.constraint import ConstraintItem
from urn.output import Output
from urn.computation import ComputationDescription


@lark.v_args(inline=True)
class BuildComputation(lark.Transformer):
    """
    Build a Computation description from a syntax tree.
    
    """
    def __init__(self):
        super().__init__()
        self.computation = ComputationDescription()
        self.output = Output()

    def start(self):
        return self

    @lark.v_args(tree=True)
    def collection(self, tree):
        self.computation.collection = dict(tree.children)
        return lark.Discard

    @lark.v_args(tree=True)
    def constraints(self, tree):
        self.computation.constraints = tree.children
        return lark.Discard
    
    def selection_size_int(self, size):
        self.computation.selection_range = range(size, size+1)
        return lark.Discard
    
    def selection_size_range(self, low, high):
        self.computation.selection_range = range(low, high+1)
        return lark.Discard

    def collection_item(self, name, number):
        return name, number
    
    @lark.v_args(tree=True)
    def count_draw(self, _):
        self.computation.computation_type = "COUNT"
        self.computation.object_type = "DRAW"
        return lark.Discard
    
    @lark.v_args(tree=True)
    def prob_draw(self, _):
        self.computation.computation_type = "PROBABILITY"
        self.computation.object_type = "DRAW"
        return lark.Discard
    
    @lark.v_args(tree=True)
    def and_constraints(self, tree):
        return tree.children

    def constraint_eq(self, name, number):
        return ConstraintItem(name, min_=number, max_=number+1)

    def constraint_lt(self, name, number):
        return ConstraintItem(name, max_=number)
    
    def constraint_gt(self, name, number):
        return ConstraintItem(name, min_=number+1)

    def constraint_le(self, name, number):
        return ConstraintItem(name, max_=number+1)

    def constraint_ge(self, name, number):
        return ConstraintItem(name, min_=number)
    
    def constraint_lt_lt(self, number_lo, name, number_hi):
        return ConstraintItem(name, min_=number_lo+1, max_=number_hi)

    def constraint_lt_le(self, number_lo, name, number_hi):
        return ConstraintItem(name, min_=number_lo+1, max_=number_hi+1)

    def constraint_le_lt(self, number_lo, name, number_hi):
        return ConstraintItem(name, min_=number_lo, max_=number_hi)

    def constraint_le_le(self, number_lo, name, number_hi):
        return ConstraintItem(name, min_=number_lo, max_=number_hi+1)

    def output_fmt(self, output):
        self.output.output_fmt = str(output).upper()
        return lark.Discard

    def output_float(self, _):
        self.output.output_float = True
        return lark.Discard

    def NUMBER(self, token):
        return int(token)

    def NAME(self, token):
        return str(token)