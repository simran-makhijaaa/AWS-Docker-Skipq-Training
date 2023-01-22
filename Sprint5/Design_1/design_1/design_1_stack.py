from aws_cdk import (
    aws_lambda as  lambda_,
    Duration,
    Stack,
    aws_iam as iam_,
    aws_cloudwatch as cw_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscription_,
    aws_apigateway as apigateway_,
)
from constructs import Construct
from resources import constants as constants

class Design1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.create_lambda_role()
        api_lambda = self.create_lambda("ApiLambda", "./resources", "api.lambda_handler",lambda_role)

        # Defining API gateway Rest Api
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html

        api = apigateway_.LambdaRestApi(self, "simranApi_design_1",
                                        handler=api_lambda,
                                        proxy=False,
                                        )

        
        # Adding resource and method in Api 
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html
        Email_response = api.root.add_resource("EmailResponse")
        Email_response.add_method("PUT")



        """ Creating SNS topic and subscriptions"""
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html

        topic = sns_.Topic(self, "DesignEmailNotifications")
        topic.add_subscription(subscription_.EmailSubscription("simran.makhija.skipq@gmail.com"))

        # taking topic arn and adding as environment variable
        topic_arn = topic.topic_arn
        api_lambda.add_environment('sns_arn',topic_arn)



        # """ Taking metric from cloud watch and creating alarm on it """
        # # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        # # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/README.html
        # dimension = {"arg1": constants.arg}
        # designMetric = cw_.Metric(
        #     namespace= constants.namespace,
        #     metric_name= constants.design_metric,
        #     dimensions_map= dimension
        #     )

        # design_alarm = cw_.Alarm(self, "Simran_Design_Alarm",
        #     comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        #     threshold=10,
        #     evaluation_periods= 1,
        #     metric= designMetric
        #     )




    """
    Createing lambda function
        Parameters:
            asset (str) - Stack file path for the application to be deployed on lambda.
            handler (str) - The name of the method within your code that Lambda calls to execute your function.
            role (str) = IAM role for lambda function.
        
        Return:
            Lambda function
    """
    def create_lambda(self, id , asset , handler , role):
        return lambda_.Function(self,
        id = id,
        code=lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_9,
        handler=handler,
        role = role,
        timeout=Duration.minutes(5))
    

    """
    Creating lambda role
        Parameters:
            assumed_by (IPrincipal) - The IAM principal which can assume this role
            managed_policies (Optional[Sequence[IManagedPolicy]]) - A list of managed policies associated with this role.
        Return:
            Role object
    """
    def create_lambda_role(self):
        lambdaRole = iam_.Role(self, "lambda-role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies = [
                                iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess")
                                ]
            )
        return lambdaRole
