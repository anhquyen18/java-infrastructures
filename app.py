#!/usr/bin/env python3
import os

import aws_cdk as cdk

from java_infrastructures.java_infrastructures_stack import JavaInfrastructuresStack
from cdk_pipeline_stack.cdk_pipeline_stack import CDKPipelineStack

app = cdk.App()
JavaInfrastructuresStack(app, "JavaInfrastructuresStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    # env=cdk.Environment(account='058264068484', region='ap-southeast-1'),
    # stack_name='github-codepipeline-stack'

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

CDKPipelineStack(app, "CDKPipelineStack",
                 env=cdk.Environment(account='058264068484', region='ap-southeast-1'),
                 stack_name='github-codepipeline-stack'
                 )

app.synth()
