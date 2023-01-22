import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from sprint4.sprint4_stack import Sprint4Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint2/sprint2_stack.py

# https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/README.html

# defining fixture
@pytest.fixture
def fixtures():
    app = core.App()
    stack = Sprint4Stack(app, "sprint4")
    template = assertions.Template.from_stack(stack)
    return template

"""
Unit test function to count lambda functions in app
"""
def test_Lambda(fixtures):    
    fixtures.resource_count_is("AWS::Lambda::Function", 3)

"""
Unit test function to count sns topics in app
"""
def test_SNS(fixtures):
    fixtures.resource_count_is("AWS::SNS::Topic", 1)

"""
Unit test function to count cloudwatch alarms in app
"""
def test_RestAPI(fixtures):
    fixtures.resource_count_is("AWS::ApiGateway::RestApi", 1)

"""
Unit test function to validate email subscription properties in app
"""
def test_Email_Subscription_Properties(fixtures):
    fixtures.has_resource_properties("AWS::SNS::Subscription", {
                                    "Protocol": "email",
                                    "TopicArn": { "Ref": "WHNotifications19AE210E"},
                                    "Endpoint": "simran.makhija.skipq@gmail.com"
                                })

"""
Unit test function to validate Dynamo DB subscription properties in app
"""
def test_DB_Subscription_Properties(fixtures):
    fixtures.has_resource_properties("AWS::SNS::Subscription", {
                                    "Protocol": "lambda",
                                    "TopicArn": { "Ref": "WHNotifications19AE210E" },
                                    "Endpoint": { "Fn::GetAtt": ["DBLambda0EC8F179", "Arn"]}
                                })

"""
Functional test for lambda role function
"""
def test_functional():
    app = core.App()
    stack = Sprint4Stack(app, "sprint4")
    lambda_role = stack.create_lambda_role
    assert lambda_role is not None

