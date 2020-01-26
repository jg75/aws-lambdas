"""Very basic calculator"""
import json
import logging

import cfnresponse


logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

    try:
        result = int(operands[0])
    except IndexError as e:
        return result

    for operand in operands[1:]:
        result = operations[operator](result, int(operand))

    return result


def get_operation(event):
    """Get the operands and operator from the event."""
    operands = event["ResourceProperties"]["Operands"]
    operator = event["ResourceProperties"]["Operator"]

    if isinstance(event["ResourceProperties"]["Operator"], list):
        operator = event["ResourceProperties"]["Operator"][0]

    return operands, operator


def lambda_handler(event, context):
    """
    Handle the lambda event.

    Get the operands and operator from the event.
    {
        Operands: List<Number>,
        Operator: + | - | * | / | %
    }
    Perform the operation on the given operands in the event.
    Send a cloudformation response if there is a response URL in the event.
    """
    operands, operator = get_operation(event)
    response = {"Value": calculate(operands, operator)}

    logger.info(f"Received: {operator} {operands}")

    if event.get("ResponseURL"):
        cfnresponse.send(event, context, cfnresponse.SUCCESS, response)

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
