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

class DeployStage(Stage):
    def __init__(self, scope: Construct, id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)
        NetworkStack(self, 'ResourceStack', env=env, stack_name="resource-stack-deploy")


class CDKPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a CodeBuild for CDK
        # build_project = codebuild.PipelineProject(self, config.BUILD_PROJECT_ID,
        #                                           environment={
        #                                               "build_image": codebuild.LinuxBuildImage.STANDARD_5_0,
        #                                               "privileged": True,
        #                                           },
        #                                           build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"))

        # Create Pipeline
        # pipeline = codepipeline.Pipeline(self, config.PIPELINE_ID, pipeline_name=config.PIPELINE_ID,
        #                                  cross_account_keys=False)
        code_pipeline = codepipeline.Pipeline(
            self, "Pipeline",
            pipeline_name="new-pipeline",
            cross_account_keys=False
        )
        # add source action
        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        git_input = pipelines.CodePipelineSource.connection(
            repo_string='anhquyen18/java-infrastructures.git',
            branch='main',
            connection_arn="arn:aws:codeconnections:ap-southeast-1:058264068484:connection/04735f98-97e7-48d3-9cd7"
                           "-32a67747277b",
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

        pipeline = pipelines.CodePipeline(
            self, 'CodePipeline',
            self_mutation=False,
            code_pipeline=code_pipeline,
            synth=synth_step,
        )

        deployment_wave = pipeline.add_wave("DeploymentWave")

        deployment_wave.add_stage(DeployStage(
            self, 'DeployStage',
            env=(Environment(account='058264068484', region='ap-southeast-1'))
        ))
