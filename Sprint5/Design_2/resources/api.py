import boto3
import os
from datetime import datetime
import json


# Get the dynamodb resource and setting the environment variable
client = boto3.resource('dynamodb', region_name='us-east-2')
api_design_table = os.environ['APIDesignTable']
table = client.Table(api_design_table)

def lambda_handler(event, context):

    method = event['httpMethod']                            # taking the http method from event
    body = event['body']                                    # taking the method body
    requestTime = event['requestContext']['requestTime']    # taking request time from event
    now = datetime.now()                                    # taking current date time
    date_ = now.isoformat()                                 # taking the date time string


    # adding attr1 and request time in our api table
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.put_item

    if method == "POST":
        json_body = json.loads(body)
        value = int(json_body[0]['event1']['attr1'])

        key = {
            "attr1": str(value),
            "requestTime": date_
        }

        response = table.put_item(Item = key,)

        if response:
            return json_response({"message": "Entered the value in the table successfully"})
        else:
            return json_response({"message": "Invalid Response"})
    
    # Reading the 10 latest events from table
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan

    elif method == "GET":
        response = table.scan(Limit=10)['Items']

        if response:
            return json_response(response)
        else:
            return json_response({"message": "The table is empty"})


# Defining the json response method for returning response in json format
def json_response(res):
    return {
        "statusCode": 200,
        "body": json.dumps(res),
        "headers": {'Content-Type': 'application/json'}
    }