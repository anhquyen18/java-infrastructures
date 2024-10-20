from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from network_stack.network_stack import NetworkStack
from ec2_stack.ec2_stack import EC2Stack
from cdk_pipeline_stack.cdk_pipeline_stack import  CDKPipelineStack

class JavaInfrastructuresStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # network_stack = NetworkStack(self, construct_id='NetworkStack', stack_name='NetworkStack')
        # EC2Stack(self, construct_id='EC2Stack', stack_name='EC2Stack', network_stack=network_stack)
        # CDKPipelineStack(self, construct_id="CDKPipelineStack", stack_name='CDKPipelineStack')
