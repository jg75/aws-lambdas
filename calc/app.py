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


def calculate(operator, operands):
    """Get the result of the operation."""
    if operator not in operations.keys():
        raise ValueError("unknown operator")

    result = int(operands[0])

    for operand in operands[1:]:
        result = operations[operator](result, int(operand))

    return result


def get_operation(event):
    """Get the operands and operator from the event."""
    resource_properties = event.get("ResourceProperties", {})
    operands = resource_properties.get("Operands", [0])
    operator = resource_properties.get("Operator")

    if isinstance(operator, list):
        operator = operator[0]

    return operator, operands


def create_response(function, *arguments):
    """
    Create the response.

    Responses
    {
        statusCode: 200,
        status: SUCCESS,
        Value: <function(*arguments)>
    }
    {
        statusCode: 400,
        status: FAILED,
        Exception: <Exception>
    }
    """
    response = {
        "statusCode": 400,
        "status": cfnresponse.FAILED
    }

    logger.info(f"Received: {arguments}")

    try:
        response["body"] = {"Value": function(*arguments)}
        response["statusCode"] = 200
        response["status"] = cfnresponse.SUCCESS
    except (ArithmeticError, ValueError) as e:
        response["exception"] = str(e)

    return response


def lambda_handler(event, context):
    """
    Handle the lambda event.

    Perform the operation on the given operands in the event and
    send a cloudformation response if there is a response URL in the event.

    Request
    {
        ResourceProperties: {
            Operator: + | - | * | / | %,
            Operands: List<Number>
        }
    }

    Response
    {
        statusCode: HTTP status code,
        body: String
    }
    """
    operator, operands = get_operation(event)
    response = create_response(calculate, operator, operands)

    if event.get("ResponseURL"):
        cfnresponse.send(event, context, response["status"], response["body"])

    return {
        "statusCode": response["statusCode"],
        "body": json.dumps(response["body"])
        if response.get("body") else response["exception"]
    }
