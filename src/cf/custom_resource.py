"""
CustomResourceHandler.

Base class for lambda backend for CloudFormation custom resources provides
methods for parsing the event object, sending a response to cloudformation,
and returning a well formed response. An overridable method `execute`, which
can be implemented by derived classes performs the `Operation` on a list of
`Operands`. A dictionary `operations` used as a registry of `Operator` -> method
mappings used by this handler.
"""
import json
import logging

from cf import cfnresponse


class CustomResourceHandler:
    """Custom Resource Handler."""

    operations = {"echo": lambda a: a}

    def __init__(self):
        """Override."""
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.setLevel(logging.INFO)

    def __call__(self, event, context):
        """Override."""
        operator, operands = self.get_operation(event)

        self.logger.info(f"Received: {operator} {operands}")

        try:
            value = self.execute(operator, operands)
        except (TypeError, LookupError, ArithmeticError, ValueError) as e:
            value = e

        self.send_cfnresponse(event, context, value)

        return self.get_response(value)

    def execute(self, operator, operands):
        """
        Execute the operation.

        You should override this function.
        """
        if operator not in self.operations.keys():
            raise ValueError("unknown operator")

        operation = self.operations[operator]
        return operation(operands)

    @staticmethod
    def get_operation(event):
        """
        Get the operands and operator from the event.

        Event
        {
            ResourceProperties: {
                Operator: + | - | * | / | % | log | etc.,
                Operands: List<Number>
            }
        }
        """
        resource_properties = event.get("ResourceProperties", {})
        operator = resource_properties.get("Operator", "")
        operands = resource_properties.get("Operands", [0])

        if type(operator) is list:
            operator = operator[0]

        if type(operands) is not list:
            operands = [operands]

        return operator, operands

    @staticmethod
    def send_cfnresponse(event, context, value):
        """Send the CloudFormation response if there is a response URL."""
        if not event.get("ResponseURL"):
            return

        response = {"Value": str(value)}
        status = cfnresponse.SUCCESS

        if isinstance(value, (Exception)):
            status = cfnresponse.FAILED

        cfnresponse.send(event, context, status, response)

    @staticmethod
    def get_response(value):
        """
        Get a properly formatted response.

        Success response
        {
            statusCode: 200,
            body: <output>
        }

        Failed response
        {
            statusCode: 400,
            body: <exception>
        }
        """
        if isinstance(value, (Exception)):
            return {
                "statusCode": 400,
                "body": json.dumps({"Value": "", "Exception": str(value)}),
            }

        return {"statusCode": 200, "body": json.dumps({"Value": value})}


handler = CustomResourceHandler()
