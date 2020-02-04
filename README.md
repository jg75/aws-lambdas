# AWS Lambdas

Topics

- [Cloudformation Integrations](#cloudformation-integrations)
  1. [Custom Resources](#custom-resources)
  2. [Custom Resource Handler](#custom-resource-handler)
  3. [Basic Calculator Handler](#basic-calculator-handler)
  4. [Network Calculator Handler](#network-calculator-handler)

---

## CloudFormation Integrations

### Custom Resources

For information about custom resources, refer to the [Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html).

---

### Custom Resource Handler

Base class for lambda backend for CloudFormation custom resources provides
methods for parsing the event object, sending a response to cloudformation,
and returning a well formed response. An overridable method `execute`, which
can be implemented by derived classes performs the `Operation` on a list of
`Operands`. A dictionary `operations` used as a registry of `Operator` to function
mappings used by this handler.

Given the following template:

```yaml
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

```python
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

```python
{
    'Value': str(operations[operator](operands))
}
```

The `Status` is captured as a string 'SUCCESS' | 'FAILED'.

The following payload will be sent to the `ResponseUrl` for cloudformation:

```python
{
{
    'Status': 'SUCCESS' or 'FAILED',
    'LogStream': context.log_stream_name,
    "PhysicalResourceId": pysical_resource_id or context.log_stream_name,
    'StackId': event['StackId'],
    'RequestId': event['RequestId'],
    'LogicalResourceId': event['LogicalResourceId'],
    'NoEcho': True | False,
    'Data': data
}
}
```

The following responses are returned by the handler.

Success response:

```python
{
    statusCode: 200,
    body: <json data>
}
```

Failed response:

```python
{
    statusCode: 400,
    body: <json data with the exception>
}
```

---

#### Basic Calculator Handler

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
 
 ---

#### Network Calculator Handler

Lambda backend for CloudFormation custom resources that do networking
related caclulations like the subnet size in bits of a given network cidr
for a specific number of subnets.

Operations:
 - SubnetSize

Operands:
 - CIDR
 - Number of subnets
