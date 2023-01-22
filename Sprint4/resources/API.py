import boto3
import os
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

""" Getting db resource and setting environment variable """
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table

client = boto3.resource('dynamodb', region_name='us-east-2')
ApiTable = os.environ['URL_key']
table = client.Table(ApiTable)

"""
Creating function to define http methods for API and return respective response

    Return:
        response in json format
"""

def lambda_handler(event, context):

    # taking the http method from event
    # taking the method body

    method = event['httpMethod']
    body = event['body']

    # Reading all the items from our dynamo db table
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan

    if method == 'GET':
        response = table.scan()['Items']
        if response:
            return json_response(response)
        else:
            return json_response({"message": "No record found"})
    
    # deleting a url from our dynamo db table
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.delete_item

    elif method == 'DELETE':
        link_id = json.loads(body)['linkId']
        response = table.delete_item(Key={"linkId": str(link_id)})
        if response:
            return json_response({"message": "Url is successfully deleted from the table"})
        else:
            return json_response({"message": "Entered url is not found in the table"})
    
    # adding a url in our dynamo db table
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.put_item
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html

    elif method == 'POST':
        link_id = json.loads(body)['linkId']
        url = json.loads(body)['URL']
        key = {
            "linkId": str(link_id),
            "URL": url
        }
        try:
            response = table.put_item(
                Item= key,
                ConditionExpression='attribute_not_exists(linkId)'
            )
            if response:
                return json_response({"message": "Added url into the table successfully"})
        except ClientError as error:
            if error.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return json_response({"message": "Link id already exists"})
    

    # updating a url in our dynamo db table
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.update_item

    elif method == 'PUT':
        link_id = json.loads(body)['linkId']
        url = json.loads(body)['URL']
        response = table.update_item(
                    Key={"linkId": str(link_id)},
                    UpdateExpression = 'SET #u=:url',
                    ConditionExpression='attribute_not_exists(deletedAt)',
                    ExpressionAttributeValues = {":url": url},
                    ExpressionAttributeNames={"#u": "URL"},
                    ReturnValues="UPDATED_NEW"
                )
        if response:
            return json_response({"message": "Updated url in the table successfully"})
        else:
            return json_response({"message": "URL not found"})
    
    # returning invalid method message to client
    else:
        return json_response({"message": "Given method is invalid. Valid methods are: GET, DELETE, POST, PUT"})


# Defining the json response method for returning response in json format
def json_response(res):
    return {
        "statusCode": 200,
        "body": json.dumps(res),
        "headers": {'Content-Type': 'application/json'}
    }



