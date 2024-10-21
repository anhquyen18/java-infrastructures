from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
)
from constructs import Construct
from network_stack.network_stack import NetworkStack
import ec2_stack.config as config

class EC2Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Scaling Group with EC2 instance running tomcat
        # self.asg = autoscaling.AutoScalingGroup(self, config.ASG, vpc=n)
