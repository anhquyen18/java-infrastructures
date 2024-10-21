#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Environment
from cdk_pipeline_stack.cdk_pipeline_stack import CDKPipelineStack
from helpers import read_yml_file

app = cdk.App()

# JavaInfrastructuresStack(app, "JavaInfrastructuresStack",
# If you don't specify 'env', this stack will be environment-agnostic.
# Account/Region-dependent features and context lookups will not work,
# but a single synthesized template can be deployed anywhere.

# Uncomment the next line to specialize this stack for the AWS Account
# and Region that are implied by the current CLI configuration.

# env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

# Uncomment the next line if you know exactly what Account and Region you
# want to deploy the stack to. */

# env=cdk.Environment(account='058264068484', region='ap-southeast-1'),
# stack_name='github-codepipeline-stack'

# For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
# )

# Define environment params from parameters.yml
dev_params = read_yml_file.read_yml_file('parameters.yml', 'dev')
test_params = read_yml_file.read_yml_file('parameters.yml', 'test')
prod_params = read_yml_file.read_yml_file('parameters.yml', 'prod')

CDKPipelineStack(app, "DevCDKPipelineStack",
                 stack_name='DevCDKPipelineStack', env_name='dev',
                 env=Environment(account=dev_params['account'], region=dev_params['region']))

app.synth()
