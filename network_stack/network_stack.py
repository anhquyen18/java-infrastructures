from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct
import network_stack.config as config


class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, env_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.env_name = env_name + '-'
        self.java_world_vpc = ec2.Vpc(self, self.env_name + config.VPC,
                                      vpc_name=self.env_name + config.VPC,
                                      ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
                                      nat_gateways=0, subnet_configuration=[],
                                      enable_dns_support=True, enable_dns_hostnames=True)

        self.elastic_ip = ec2.CfnEIP(self, "EIP")
        self.internet_gateway = self.attach_internet_gateway()
        self.subnet_id_to_subnet_map = {}
        self.route_table_id_to_route_table_map = {}
        self.create_route_tables()
        self.create_subnets()
        # self.create_subnet_route_table_associations()
        # self.nat_gateway = self.attach_nat_gateway()
        # self.nat_gateway.add_dependency(self.elastic_ip)
        # self.create_routes()

    def create_routes(self):
        # Create routes of the route table
        for route_table_id, routes in config.ROUTE_TABLES_ID_TO_ROUTES_MAP.items():
            for i in range(len(routes)):
                route = routes[i]
                kwargs = {
                    **route,
                    'route_table_id': self.route_table_id_to_route_table_map[route_table_id].ref,
                }
                if route['router_type'] == ec2.RouterType.GATEWAY:
                    kwargs['gateway_id'] = self.internet_gateway.ref
                if route['router_type'] == ec2.RouterType.NAT_GATEWAY:
                    kwargs['nat_gateway_id'] = self.nat_gateway.ref
                del kwargs['router_type']
                ec2.CfnRoute(self, f'{route_table_id}-route-{i}', **kwargs)

    def attach_nat_gateway(self):
        # Create and attach nat gateway to the Vpc
        nat_gateway = ec2.CfnNatGateway(self, self.env_name + config.NAT_GATEWAY,
                                        allocation_id=self.elastic_ip.attr_allocation_id,
                                        subnet_id=self.subnet_id_to_subnet_map[config.PUBLIC_SUBNET_1a].ref)
        return nat_gateway

    def create_subnet_route_table_associations(self):
        for subnet_id, subnet_config in config.SUBNET_CONFIGURATION.items():
            route_table_id = subnet_config['route_table_id']
            ec2.CfnSubnetRouteTableAssociation(
                self, f'{subnet_id}-{route_table_id}',
                subnet_id=self.subnet_id_to_subnet_map[subnet_id].ref,
                route_table_id=self.route_table_id_to_route_table_map[route_table_id].ref,
            )

    def create_subnets(self):
        # Create subnets of the VPC
        for subnet_id, subnet_config in config.SUBNET_CONFIGURATION.items():
            subnet = ec2.CfnSubnet(
                self, subnet_id, vpc_id=self.java_world_vpc.vpc_id,
                cidr_block=subnet_config['cidr_block'],
                availability_zone=subnet_config['availability_zone'],
                tags=[{'key': 'Name', 'value': self.env_name + subnet_id}],
                map_public_ip_on_launch=subnet_config['map_public_ip_on_launch'],
            )
            self.subnet_id_to_subnet_map[subnet_id] = subnet

    def create_route_tables(self):
        # Create route tables
        for route_table_id in config.ROUTE_TABLES_ID_TO_ROUTES_MAP:
            self.route_table_id_to_route_table_map[route_table_id] = ec2.CfnRouteTable(
                self, route_table_id, vpc_id=self.java_world_vpc.vpc_id,
                tags=[{'key': 'Name', 'value': self.env_name + route_table_id}],
            )

    def attach_internet_gateway(self) -> ec2.CfnInternetGateway:
        # Create and attach internet gateway to the VPC
        internet_gateway = ec2.CfnInternetGateway(self, self.env_name + config.INTERNET_GATEWAY)
        ec2.CfnVPCGatewayAttachment(self, 'internet-gateway-attachment',
                                    vpc_id=self.java_world_vpc.vpc_id,
                                    internet_gateway_id=internet_gateway.ref)
        return internet_gateway
