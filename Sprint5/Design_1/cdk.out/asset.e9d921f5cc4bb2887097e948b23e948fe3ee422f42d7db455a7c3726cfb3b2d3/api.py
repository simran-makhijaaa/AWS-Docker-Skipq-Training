from cloudwatch_putData import AWSCloudWatch
import constants as constants

def lambda_handler(event, context):
    
    """CloudWatch object"""
    cloudwatch_object = AWSCloudWatch()
    
    body = event["body"]
    value = int(body)
    # constants.arg = arg_str
    
     """ Sending data to CloudWatch"""
    dimensions = [{'Name': 'arg1','Value': str(value)}]

    cloudwatch_object.cloudwatch_metric_data(constants.namespace , constants.design_metric , dimensions, value)

    if event["httpMethod"] == "PUT":
        response = {
            "statusCode": 200,
            "body": event["body"],
        }

        return response
