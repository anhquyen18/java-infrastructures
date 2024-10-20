from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from java_infrastructures.network_stack import NetworkStack


class JavaInfrastructuresStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        NetworkStack(self, construct_id='NetworkStack', stack_name='NetworkStack')
        # example resource
        # queue = sqs.Queue(
        #     self, "JavaInfrastructuresQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
