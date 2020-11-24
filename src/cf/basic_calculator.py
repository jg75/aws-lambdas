"""
BasicCalculator.

Lambda backend for CloudFormation custom resources
providing basic calculator functions.
"""
from functools import reduce
from operator import add, floordiv, mod, mul, sub

from cf.custom_resource import CustomResourceHandler


class BasicCalculator(CustomResourceHandler):
    """Support basic calculator operations."""

    operations = {"+": add, "-": sub, "*": mul, "/": floordiv, "%": mod}

    def execute(self, operator, operands):
        """Execute the operation."""
        try:
            return reduce(self.operations[operator], [int(i) for i in operands])
        except KeyError:
            raise ValueError("unknown operator")


handler = BasicCalculator()
