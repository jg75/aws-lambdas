"""Very basic calculator"""
from json import dumps


operations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b,
    "%": lambda a, b: a % b,
}


def calculate(operands, operator):
    """Get the result of the operation."""
    result = 0

    if len(operands) and operator in operations.keys():
        result = int(operands[0])

        for operand in operands[1:]:
            result = operations[operator](result, int(operand))

    return result


def response(body, status=200):
    """Get a properly formatted response."""
    return {"statusCode": status, "body": dumps(body)}


def lambda_handler(event, context):
    """
    Handle the lambda event.

    Perform the operation on the given operands in the event.
    {
        Operands: List<Number>,
        Operator: + | - | * | / | %
    }
    """
    operands = event["ResourceProperties"]["Operands"]
    operator = event["ResourceProperties"]["Operator"]
    body = {"Value": calculate(operands, operator)}

    return response(body)
