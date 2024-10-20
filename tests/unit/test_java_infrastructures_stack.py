import aws_cdk as core
import aws_cdk.assertions as assertions

from java_infrastructures.java_infrastructures_stack import JavaInfrastructuresStack

# example tests. To run these tests, uncomment this file along with the example
# resource in java_infrastructures/java_infrastructures_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = JavaInfrastructuresStack(app, "java-infrastructures")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
