import network_stack.config as network_config

PROJECT_NAME = network_config.PROJECT_NAME

# build project
BUILD_PROJECT_ID = PROJECT_NAME + '-' + 'cdk-build-project'
PIPELINE_ID = PROJECT_NAME + '-' + 'cdk-pipeline'

# connection arn
GITHUB_CONNECTION_ARN = 'arn:aws:codeconnections:ap-southeast-1:058264068484:connection/db1d7cc2-7cce-4e51-a9c9-8f0a4eb951f6'
REPO = 'anhquyen18/java-infrastructures'