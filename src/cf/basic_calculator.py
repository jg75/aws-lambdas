"""Lambda handler for CloudFormation custom resources."""
from src.cf.custom_resource import CustomResourceHandler


class BasicCalculator(CustomResourceHandler):
    """
    Support basic calculator operations.
    """

    operations = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a // b,
        "%": lambda a, b: a % b,
    }

    def execute(self, operator, operands):
        """Execute the operation."""
        if operator not in self.operations.keys():
            raise ValueError("unknown operator")

        result = int(operands[0])
        operation = self.operations[operator]

        for operand in operands[1:]:
            result = operation(result, int(operand))

        return result


handler = BasicCalculator()
