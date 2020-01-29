"""
CustomResourceHandler.

Base class for lambda backend for CloudFormation custom resources provides
methods for parsing the event object, sending a response to cloudformation,
and returning a well formed response. An overridable method `execute`, which
can be implemented by derived classes performs the `Operation` on a list of
`Operands`. A dictionary `operations` used as a registry of `Operator` -> method
mappings used by this handler.

For information about custom resources, see here:
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html

Given the following template:
```
Parameters:
  MyCustomResourceFunction:
    Description: Custom resource handler function Arn
    Type: AWS::SSM::Parameter::Value<String>
    Default: /MyCommonFunctions/MyCustomResourceFunction

Resources:
  MyEcho:
    Type: Custom::Echo
    Properties:
      ServiceToken: !Ref MyCustomResourceFunction
      Operator: echo
      Operands:
        - this is a
        - test

Outputs:
  Echo:
    Description: The output of the custom resource
    Value: !GetAtt MyEcho.Value
```

The following will be included in the lambda `event`.
```
    {
        'ResponseURL': 'http://pre-signed-S3-url-for-response',
        'StackId' : 'arn:aws:cloudformation:us-west-2:123456789012:stack/stack-name/guid',
        'RequestId' : 'unique id for this create request',
        'ResourceType' : 'Custom::Echo',
        'LogicalResourceId' : 'MyEcho',
        'ResourceProperties': {
            'Operator': 'echo',
            'Operands': ['this is a', 'test']
        }
    }
```

The `Data` response data of the `execute` method is put into a dictionary as
a string.
```
    {
        'Value': str(operations[operator](operands))
    }
```

The `Status` is captured as a string 'SUCCESS' | 'FAILED'.

The following payload will be sent to the `ResponseUrl` for cloudformation.
```
    {
        'Status': <str>
        'LogStream': context.log_stream_name,
        "PhysicalResourceId": <str> | context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'NoEcho': True | False,
        'Data': <dict>
    }
```

The following responses are returned by the handler.

Success response:
```
    {
        statusCode: 200,
        body: <json data>
    }
```

Failed response:
```
    {
        statusCode: 400,
        body: <json data with the exception>
    }
```
"""
import json
import logging

from src.cf import cfnresponse


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
