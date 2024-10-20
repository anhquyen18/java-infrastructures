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


class DeploymentStage(Stage):
    def __init__(self, scope: Construct, id: str, env: Environment, env_name: str, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)
        NetworkStack(self, 'NetworkStack', env=env, env_name=env_name, stack_name=env_name + '-NetworkStack')


class CDKPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a pipeline for CDK app
        code_pipeline = codepipeline.Pipeline(
            self, config.PIPELINE_ID,
            pipeline_name=config.PIPELINE_ID,
            cross_account_keys=False
        )

        # Create pipeline source
        # Need to create a connection between AWS and Github account by Console before create this one
        git_input = pipelines.CodePipelineSource.connection(
            repo_string='anhquyen18/java-infrastructures',
            branch='dev',
            connection_arn="arn:aws:codeconnections:ap-southeast-1:058264068484:connection/db1d7cc2-7cce-4e51-a9c9-8f0a4eb951f6",
        )

        test_git_input = pipelines.CodePipelineSource.connection(
            repo_string='anhquyen18/java-infrastructures',
            branch='test',
            connection_arn="arn:aws:codeconnections:ap-southeast-1:058264068484:connection/db1d7cc2-7cce-4e51-a9c9-8f0a4eb951f6",
        )

        synth_step = pipelines.ShellStep(
            id="Synth",
            install_commands=[
                'pip install -r requirements.txt'
            ],
            commands=[
                'npx cdk synth'
            ],
            input=git_input
        )

        test_synth_step = pipelines.ShellStep(
            id="Synth",
            install_commands=[
                'pip install -r requirements.txt'
            ],
            commands=[
                'npx cdk synth'
            ],
            input=git_input
        )

        pipeline = pipelines.CodePipeline(
            self, 'CDKDevCodePipeline',
            self_mutation=False,
            code_pipeline=code_pipeline,
            synth=synth_step,
        )

        test_pipeline = pipelines.CodePipeline(
            self, 'CDKTestCodePipeline',
            self_mutation=False,
            code_pipeline=code_pipeline,
            synth=synth_step,
        )

        deployment_wave = pipeline.add_wave("DeploymentWave")

        deployment_wave.add_stage(DeploymentStage(
            self, 'Dev',
            env_name='dev',
            env=(Environment(account='058264068484', region='ap-southeast-1')),
        ))

        deployment_wave.add_stage(DeploymentStage(
            self, 'Test',
            env_name='test',
            env=(Environment(account='058264068484', region='ap-southeast-1')),
        ))

        # deployment_wave.add_stage(DevStage(
        #     self, 'DevStage',
        #     env=(Environment(account='058264068484', region='ap-southeast-1', stage='dev'))
        # ))
