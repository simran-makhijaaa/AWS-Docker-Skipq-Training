from cloudwatch_putData import AWSCloudWatch
import constants as constants

def lambda_handler(event, context):
    
    """CloudWatch object"""
    cloudwatch_object = AWSCloudWatch()
    
    arg_str = event["arg1"]
    arg = int(arg_str)
    constants.arg = arg_str
    
     """ Sending data to CloudWatch"""
    dimensions = [{'Name': 'arg1','Value': str(arg)}]

    cloudwatch_object.cloudwatch_metric_data(constants.namespace , constants.design_metric , dimensions, arg)

    if event["httpMethod"] == "PUT":
        response = {
            "statusCode": 200,
            "body": event["body"],
        }

        return response
