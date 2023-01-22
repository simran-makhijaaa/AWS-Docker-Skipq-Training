import boto3
import os


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table


def lambda_handler(event, context):
    client =boto3.resource('dynamodb', region_name='us-east-2')
    dbTable = os.environ['DynamoDbAlarmTable']
    table=client.Table(dbTable)
    message_id = event["Records"][0]["Sns"]["MessageId"]
    timestamp = event["Records"][0]["Sns"]["Timestamp"]
    response=table.put_item(Item={"id": message_id, "Timestamp": timestamp})