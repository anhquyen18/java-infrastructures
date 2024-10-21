import os

from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    pipelines,
    Stage,
    Environment,
)
from constructs import Construct
import cdk_pipeline_stack.config as config
from network_stack.network_stack import NetworkStack
from helpers import read_yml_file


class DeploymentStage(Stage):
    def __init__(self, scope: Construct, id: str, env: Environment, env_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        NetworkStack(self, env_name.capitalize() + 'NetworkStack', env=env, env_name=env_name,
                     stack_name=env_name.capitalize() + 'NetworkStack')


class CDKPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, env_name: str, manual_approve: bool, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.env_name_id = env_name + '-'

        # Read parameters for separate environment from parameters.yml
        parameters = read_yml_file.read_yml_file('parameters.yml', env_name)

        # Create a pipeline for CDK
        code_pipeline = codepipeline.Pipeline(
            self, env_name.capitalize() + config.PIPELINE_ID,
            pipeline_name=self.env_name_id + config.PIPELINE_ID,
            cross_account_keys=False
        )

        # Create pipeline source
        # Need to create a connection between AWS and Github account by Console before create this one
        git_input = pipelines.CodePipelineSource.connection(
            repo_string=config.REPO,
            branch=env_name,
            connection_arn=config.GITHUB_CONNECTION_ARN,
        )

        # Create shell command stage
        synth_step = pipelines.ShellStep(
            id=env_name.capitalize() + "Synth",
            install_commands=[
                'pip install -r requirements.txt'
            ],
            commands=[
                'npx cdk synth'
            ],
            input=git_input
        )

        # Add pipeline
        pipeline = pipelines.CodePipeline(
            self, env_name.capitalize() + 'CDKCodePipeline',
            self_mutation=False,
            code_pipeline=code_pipeline,
            synth=synth_step,
        )

        # Add deployment stage
        deployment_wave = pipeline.add_wave("DeploymentWave")
        if manual_approve:
            deployment_wave.add_stage(DeploymentStage(
                self, env_name.capitalize(),
                env_name=env_name,
                env=Environment(account=parameters['account'], region=parameters['region'])
            ), pre=[pipelines.ManualApprovalStep("DeployStack")])
        else:
            deployment_wave.add_stage(DeploymentStage(
                self, env_name.capitalize(),
                env_name=env_name,
                env=Environment(account=parameters['account'], region=parameters['region'])
            ))
