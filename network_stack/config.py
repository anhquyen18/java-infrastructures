from aws_cdk import (
    aws_ec2 as ec2,
)

PROJECT_NAME = 'java-world'
VPC = PROJECT_NAME + '-' + 'vpc'

INTERNET_GATEWAY = PROJECT_NAME + '-' + 'internet-gateway'
NAT_GATEWAY = PROJECT_NAME + '-' + 'nat-gateway'
REGION = 'ap-southeast-1'

PUBLIC_ROUTE_TABLE = PROJECT_NAME + '-' + 'public-route-table'
PRIVATE_ROUTE_TABLE = PROJECT_NAME + '-' + 'private-route-table'

# route tables
ROUTE_TABLES_ID_TO_ROUTES_MAP = {
    PUBLIC_ROUTE_TABLE: [
        {
            'destination_cidr_block': '0.0.0.0/0',
            'gateway_id': INTERNET_GATEWAY,
            'router_type': ec2.RouterType.GATEWAY
        }
    ],
    PRIVATE_ROUTE_TABLE: [
        {
            'destination_cidr_block': '0.0.0.0/0',
            'nat_gateway_id': NAT_GATEWAY,
            'router_type': ec2.RouterType.NAT_GATEWAY
        }
    ],
}

# subnets
PUBLIC_SUBNET = PROJECT_NAME + '-' + 'public-subnet'
PRIVATE_SUBNET = PROJECT_NAME + '-' + 'private-subnet'

SUBNET_CONFIGURATION = {
    PUBLIC_SUBNET: {
        'availability_zone': 'ap-southeast-1a',
        'cidr_block': '10.0.1.0/24',
        'map_public_ip_on_launch': True,
        'route_table_id': PUBLIC_ROUTE_TABLE,
    },
    PRIVATE_SUBNET: {
        'availability_zone': 'ap-southeast-1b',
        'cidr_block': '10.0.2.0/24',
        'map_public_ip_on_launch': False,
        'route_table_id': PRIVATE_ROUTE_TABLE,
    }
}
