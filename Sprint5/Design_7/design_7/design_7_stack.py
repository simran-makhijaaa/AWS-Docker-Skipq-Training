from aws_cdk import (
    aws_lambda as  lambda_,
    Duration,
    Stack,
    aws_iam as iam_,
    aws_apigateway as apigateway_,
    RemovalPolicy,
    aws_s3 as s3_,
)
from constructs import Construct

class Design7Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.create_lambda_role()
        fn = self.create_lambda("LargeFileLambda", "./resources", "largefile.lambda_handler",lambda_role)


        # Defining API gateway Rest Api
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html

        api = apigateway_.LambdaRestApi(self, "simranApi_design_7",
                                        handler=fn,
                                        proxy=False,
                                        )
        

        # Adding resource and method in Api 
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html
        items = api.root.add_resource("largeFiles")
        items.add_method("GET")



        # Creating s3 bucket and giving read write permission for our lambda function 
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3/README.html
        bucket = s3_.Bucket(self, "SimranDesign7Bucket")
        bucket.grant_read_write(fn)

        # Adding bucket to environment variable
        fn.add_environment('Design7Bucket',bucket.bucket_name)

    







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
                                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),                                
                                ]
            )
        return lambdaRole
