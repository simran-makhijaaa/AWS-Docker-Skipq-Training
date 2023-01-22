import aws_cdk as core
import aws_cdk.assertions as assertions

from design_7.design_7_stack import Design7Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in design_7/design_7_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Design7Stack(app, "design-7")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
