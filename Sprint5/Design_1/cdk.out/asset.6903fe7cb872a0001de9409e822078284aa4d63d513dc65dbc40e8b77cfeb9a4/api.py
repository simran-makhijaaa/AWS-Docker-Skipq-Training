from cloudwatch_putData import AWSCloudWatch
import constants as constants

def lambda_handler(event, context):
    
    """CloudWatch object"""
    cloudwatch_object = AWSCloudWatch()
    
    body = event['body']
    arg = int(body[8:])
    
     """ Sending data to CloudWatch"""
    constants.dimensions = [{'Name': 'arg1','Value': str(arg)}]

    cloudwatch_object.cloudwatch_metric_data(constants.namespace , constants.design_metric , constants.dimensions, arg)

    if event["httpMethod"] == "PUT":
        response = {
            "statusCode": 200,
            "body": event["body"],
        }

        return response
