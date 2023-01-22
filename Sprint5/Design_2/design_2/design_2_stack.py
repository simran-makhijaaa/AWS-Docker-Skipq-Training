from aws_cdk import (
    aws_lambda as  lambda_,
    Duration,
    Stack,
    aws_iam as iam_,
    aws_cloudwatch as cw_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscription_,
    aws_apigateway as apigateway_,
    aws_dynamodb as db_,
    RemovalPolicy,
)
from constructs import Construct

class Design2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.create_lambda_role()
        api_lambda = self.create_lambda("ApiLambda", "./resources", "api.lambda_handler",lambda_role)

        
        """
            - Calling design api table
            - giving read write access to table
            - adding api lambda to environment variable
        """
        api_design_table = self.create_design_api_table()
        api_design_table.grant_read_write_data(api_lambda)
        api_lambda.add_environment('APIDesignTable',api_design_table.table_name)


        # Defining API gateway Rest Apis
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html

        api_1 = apigateway_.LambdaRestApi(self, "simranApi_design_2_1",
                                        handler=api_lambda,
                                        proxy=False,
                                        )

        
        api_2 = apigateway_.LambdaRestApi(self, "simranApi_design_2_2",
                                        handler=api_lambda,
                                        proxy=False,
                                        )

        
        # Adding resource and method in Api 
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html
        items = api_1.root.add_resource("root")
        items.add_method("GET")
        items.add_method("POST")

        items = api_2.root.add_resource("root")
        items.add_method("GET")
        items.add_method("POST")




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
                                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"),
                                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
                                ]
            )
        return lambdaRole
    

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/README.html
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Attribute.html#aws_cdk.aws_dynamodb.Attribute
    """
    Creating dynamo db table
        Parameters:
            partition_key (Union[Attribute, Dict[str, Any]]) - Partition key attribute definition.
            removal_policy (Optional[RemovalPolicy]) - The removal policy to apply to the DynamoDB Table.
            sort_key (Union[Attribute, Dict[str, Any], None]) - Sort key attribute definition.
        Return:
            table
    """
    def create_design_api_table(self):
        table = db_.Table(self, "DesignAPITable",
            partition_key = db_.Attribute(name="attr1", type=db_.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,
            sort_key = db_.Attribute(name="requestTime",type=db_.AttributeType.STRING),
        )
        return table
