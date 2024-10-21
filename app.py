#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Environment
from cdk_pipeline_stack.cdk_pipeline_stack import CDKPipelineStack
from helpers import read_yml_file

app = cdk.App()

# Define environment params from parameters.yml
dev_params = read_yml_file.read_yml_file('parameters.yml', 'dev')
test_params = read_yml_file.read_yml_file('parameters.yml', 'test')

CDKPipelineStack(app, "DevCDKPipelineStack",
                 stack_name='DevCDKPipelineStack', env_name='dev',
                 manual_approve=False,
                 env=Environment(account=dev_params['account'], region=dev_params['region']))
CDKPipelineStack(app, "TestCDKPipelineStack",
                 stack_name='TestCDKPipelineStack', env_name='test',
                 manual_approve=True,
                 env=Environment(account=test_params['account'], region=test_params['region']))

app.synth()
