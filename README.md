# aws-lambdas

## CustomResourceHandler

Base class for lambda backend for CloudFormation custom resources provides
methods for parsing the event object, sending a response to cloudformation,
and returning a well formed response. An overridable method `execute`, which
can be implemented by derived classes performs the `Operation` on a list of
`Operands`. A dictionary `operations` used as a registry of `Operator` -> method
mappings used by this handler.

For information about custom resources, see [here](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html)

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

The following will be included in the lambda `event`:

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
a string:

```
    {
        'Value': str(operations[operator](operands))
    }
```

The `Status` is captured as a string 'SUCCESS' | 'FAILED'.

The following payload will be sent to the `ResponseUrl` for cloudformation:
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

## BasicCalculatorHandler

Lambda backend for CloudFormation custom resources
providing basic calculator functions.

Operations:
 - + 
 - -
 - *
 - /
 - %

Operands:
 - Number(s)

## NetworkCalculatorHandler

Lambda backend for CloudFormation custom resources that do networking
related caclulations like the subnet size in bits of a given network cidr
for a specific number of subnets.

Operations:
 - SubnetSize

Operands:
 - CIDR
 - Number of subnets
