"""Very basic calculator"""
import cfnresponse
import logging


operations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b,
    "%": lambda a, b: a % b,
}
logger = logging.getLogger()

logger.setLevel(logging.INFO)


def calculate(operands, operator):
    """Get the result of the operation."""
    result = 0

    try:
        result = int(operands[0])
    except IndexError as e:
        return result

    for operand in operands[1:]:
        result = operations[operator](result, int(operand))

    return result


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

    if isinstance(operator, list):
        operator = operator[0]

    logging.info(f"{operands} {operator}")

    value = calculate(operands, operator)

    logging.info(value)

    cfnresponse.send(event, context, cfnresponse.SUCCESS, {"Value": value})
