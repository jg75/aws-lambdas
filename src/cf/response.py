"""The CloudFormation response."""
import json
import logging
import requests
from requests.exceptions import RequestException


SUCCESS = "SUCCESS"
FAILED = "FAILED"


class CloudFormationResponse:
    """
    Responsible for creating a properly formatted CloudFormation response.
    """

    def __init__(self):
        """Override init."""
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.setLevel(logging.INFO)

    def send(self, *args, **kwargs):
        """
        Send a properly formatted response.

        {
            Status: SUCCESS | FAILED,
            Reason: Log Stream: context.log_stream_name,
            PhysicalResourceId: <str> | context.log_stream_name,
            StackId: event['StackId'],
            RequestId: event['RequestId'],
            LogicalResourceId: event['LogicalResourceId'],
            NoEcho: True | False,
            Data: <dict>
        }
        """
        event, context, status, data = args
        response_url = event["ResponseURL"]
        log_stream = context.log_stream_name
        physical_resource_id = kwargs.get("physical_resource_id", log_stream)
        no_echo = kwargs.get("no_echo", False)
        body = json.dumps(
            {
                "Status": status,
                "Reason": f"See log stream: {log_stream}",
                "PhysicalResourceId": physical_resource_id,
                "StackId": event["StackId"],
                "RequestId": event["RequestId"],
                "LogicalResourceId": event["LogicalResourceId"],
                "NoEcho": no_echo,
                "Data": data,
            }
        )
        headers = {"Content-Type": "", "Content-Length": str(len(body))}

        try:
            response = requests.put(response_url, data=body, headers=headers)

            self.logger.info(response.reason)
        except RequestException as e:
            self.logger.info(f"Payload: {body}")
            self.logger.error(f"{e.__class__.__name__}: {str(e)}: {response_url}")
