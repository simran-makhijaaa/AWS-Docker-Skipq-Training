from aws_cdk import (
    aws_lambda as  lambda_,
    Duration,
    aws_events as events_,
    aws_events_targets as target_,
    RemovalPolicy,
    Stack,
    aws_iam as iam_,
    aws_cloudwatch as cw_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscription_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as db_,
    aws_codedeploy as codedeploy_,
    aws_apigateway as apigateway_
    
)
from constructs import Construct
from resources import constants as constants

class Sprint4Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.create_lambda_role()
        fn = self.create_lambda("WHapp", "./resources", "WHapp.lambda_handler",lambda_role)
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
        dbLambda = self.create_lambda("DBLambda", "./resources", "DBapp.lambda_handler",lambda_role)
        ApiLambda = self.create_lambda("APILambda", "./resources", "API.lambda_handler", lambda_role)



        """
            - Calling dynamodb table
            - giving read write access to table
            - adding db lambda to environment variable
        """
        dbTable = self.create_dynamodb_table()
        dbTable.grant_read_write_data(dbLambda)
        dbLambda.add_environment('DynamoDbAlarmTable',dbTable.table_name)



        """
            - Calling API table
            - giving read write access to table
            - adding api and whapp lambda functions to environment variable
        """
        ApiTable = self.create_API_table()
        ApiTable.grant_read_write_data(ApiLambda)
        ApiLambda.add_environment('URL_key',ApiTable.table_name)
        fn.add_environment('URL_key', ApiTable.table_name)


        # Defining API gateway Rest Api
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html

        api = apigateway_.LambdaRestApi(self, "simranApi",
                                        handler=ApiLambda,
                                        proxy=False,
                                        endpoint_configuration=apigateway_.EndpointConfiguration(
                                                                types=[apigateway_.EndpointType.REGIONAL]
                                                            )
                                        )

        # Giving permission to API gateway for invoking APi lambda function
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html#aws_cdk.aws_lambda.Function.grant_invoke
        
        ApiLambda.grant_invoke(iam_.ServicePrincipal("apigateway.amazonaws.com"))

        # Adding the CRUD methods in Api 
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html
        items = api.root.add_resource("items")
        items.add_method("GET")
        items.add_method("POST")
        items.add_method("DELETE")
        items.add_method("PUT")




        # Creating duration and error metric of lambda function
        duration_metric = fn.metric_duration()
        invocation_metric = fn.metric_invocations()



        # Creating alarms for duration and error metrics
        duration_alarm = cw_.Alarm(self, "Duration_Errors",
                comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold=0.9,
                evaluation_periods= 60,
                metric= duration_metric
                )


        invocation_alarm = cw_.Alarm(self, "Invocation_Errors",
                comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold=2,
                evaluation_periods= 60,
                metric= invocation_metric
                )
        
        # making sure each CDK synthesize produces a different version
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentConfig.html
        version = fn.current_version
        alias = lambda_.Alias(self, "versionAlias",
            alias_name="prod",
            version=version
            )

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentConfig.html
        deployment_group = codedeploy_.LambdaDeploymentGroup(self, "codeDeploymentGroup",
                            # application=application,
                            alarms = [duration_alarm,invocation_alarm],
                            alias=alias,
                            # auto_rollback = codedeploy_.AutoRollbackConfig(deployment_in_alarm=True),
                            deployment_config=codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE
                        )



        # Scheduling the cron job for 1 hour interval
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Schedule.html
        schedule = events_.Schedule.rate(Duration.minutes(60))
        
        # targeting to the event
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events_targets/LambdaFunction.html
        target = target_.LambdaFunction(handler = fn)

        # defining rule as an eventbridge between schedule and target
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/README.html
        rule = events_.Rule(self, "WHapprule",
            schedule = schedule,
            targets=[target])
        rule.apply_removal_policy(RemovalPolicy.DESTROY)

        """ Creating SNS topic and subscriptions"""
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html

        topic = sns_.Topic(self, "WHNotifications")
        topic.add_subscription(subscription_.EmailSubscription("simran.makhija.skipq@gmail.com"))
        topic.add_subscription(subscription_.LambdaSubscription(dbLambda))
        

        """ Two alarms are created for websites's availability and latency """
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/README.html

        
        for index, url in enumerate(constants.urls,start=1):
            """ Alarm for Availability """

            dimensions = {'URL': url}
            availibilty_metric = cw_.Metric(
                namespace= constants.namespace,
                metric_name= constants.AvailibiltyMetric,
                dimensions_map= dimensions
                )

            availability_alarm = cw_.Alarm(self, "Availibilty_Errors_" + str(index),
                comparison_operator=cw_.ComparisonOperator.LESS_THAN_THRESHOLD,
                threshold=1,
                evaluation_periods= 60,
                metric= availibilty_metric
                )

            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            availability_alarm.add_alarm_action(actions_.SnsAction(topic))
            
            """ Alarm for Latency """

            latency_metric = cw_.Metric(
                namespace= constants.namespace,
                metric_name= constants.LatencyMetric,
                dimensions_map= dimensions
                )

            latency_alarm = cw_.Alarm(self, "Latency_Errors_" + str(index),
                comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold=0.5,
                evaluation_periods= 60,
                metric= latency_metric
                )
            
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            latency_alarm.add_alarm_action(actions_.SnsAction(topic))

        

    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html

    """
    Createing lambda function

        Parameters:
            asset (str) - Stack file path for the application to be deployed on lambda.
            handler (str) - The name of the method within your code that Lambda calls to execute your function.
            role (str) = IAM role for lambda function.
        
        Return:
            Lambda function
    """
    def create_lambda(self,id , asset , handler , role):
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
                                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
                                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess")
                            ]
            )
        return lambdaRole

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/README.html
    """
    Creating dynamo db table
        Parameters:
            partition_key (Union[Attribute, Dict[str, Any]]) - Partition key attribute definition.
            removal_policy (Optional[RemovalPolicy]) - The removal policy to apply to the DynamoDB Table.
            sort_key (Union[Attribute, Dict[str, Any], None]) - Sort key attribute definition.

        Return:
            table
    """
    def create_dynamodb_table(self):
        table = db_.Table(self, "DynamoDbAlarmTable",
            partition_key = db_.Attribute(name="Message_id", type=db_.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,
            sort_key = db_.Attribute(name="Timestamp",type=db_.AttributeType.STRING),
        )
        return table
    

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/README.html
    """
    Creating API table for Lambda URL
        Parameters:
            partition_key (Union[Attribute, Dict[str, Any]]) - Partition key attribute definition.
            removal_policy (Optional[RemovalPolicy]) - The removal policy to apply to the DynamoDB Table.

        Return:
            table
    """
    def create_API_table(self):
        table = db_.Table(self, "APIUrlTable",
            partition_key = db_.Attribute(name="linkId", type=db_.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY
        )
        return table


