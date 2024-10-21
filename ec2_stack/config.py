import network_stack.config as network_config

PROJECT_NAME = network_config.PROJECT_NAME

# Auto scaling group
ASG_ID = PROJECT_NAME + '-' + 'asg'
ELB_ID = PROJECT_NAME + '-' + 'elb'