import aws_cdk as core
import aws_cdk.assertions as assertions

from design_5.design_5_stack import Design5Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in design_5/design_5_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Design5Stack(app, "design-5")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
