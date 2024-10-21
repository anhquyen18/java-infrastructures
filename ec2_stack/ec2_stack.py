from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elb,
    CfnOutput,
)
from constructs import Construct
from network_stack.network_stack import NetworkStack
import ec2_stack.config as ec2_config
import network_stack.config as network_config


class EC2Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, network_stack: NetworkStack, env_name: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.env_name_id = env_name + '-'

        # Create Scaling Group
        asg = autoscaling.AutoScalingGroup(self, env_name.capitalize() + ec2_config.ASG_ID,
                                           vpc=network_stack.vpc,
                                           instance_type=ec2.InstanceType("t2.micro"),
                                           machine_image=ec2.MachineImage.latest_amazon_linux(),
                                           min_capacity=1,
                                           max_capacity=3)

        # Create Elastic Load Balancer (ELB)
        lb = elb.ApplicationLoadBalancer(self, env_name.capitalize() + ec2_config.ELB_ID,
                                         vpc=network_stack.vpc,
                                         internet_facing=True,
                                         vpc_subnets=[
                                             network_stack.subnet_id_to_subnet_map[network_config.PUBLIC_SUBNET_1a],
                                             network_stack.subnet_id_to_subnet_map[
                                                 network_config.PUBLIC_SUBNET_1b]]
                                         )

        # Add listener to Load Balancer
        listener = lb.add_listener("Listener", port=80)

        # Tạo Target Group cho ASG
        target_group = listener.add_targets("ApplicationFleet",
                                            port=80,
                                            targets=[asg])

        # Allow ELB access to port 80 on instances
        asg.connections.allow_from(lb, ec2.Port.tcp(80), "Allow traffic from ALB")

        CfnOutput(self, "LoadBalancerDNS",
                  value=lb.load_balancer_dns_name)
