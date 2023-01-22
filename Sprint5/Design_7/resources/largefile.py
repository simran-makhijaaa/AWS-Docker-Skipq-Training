import boto3
import os
import json

"""
Calling s3 client
calling bucket environment variable
"""
client = boto3.client('s3', region_name ='us-east-2')
bucket = os.environ['Design7Bucket']


def lambda_handler(event, context):

    # defining file name and bucket and passing it to our presigned_post function
    # and getting presigned url for s3 bucket
    object_name= 'image.png'
    bucket_name= bucket
    method = event['httpMethod']
    response=create_presigned_post(bucket_name, object_name, 3600)

    if method == "GET":
        return {
            'statusCode': 200,
            'body': json.dumps(response),
            'headers': {'Content-Type': 'application/json'}
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Invalid method, please call get method"}),
            'headers': {'Content-Type': 'application/json'}
        }


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html#generating-a-presigned-url-to-upload-a-file

"""Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
"""

def create_presigned_post(bucket_name, object_name, expiration):

    # Generate a presigned S3 POST URL
    try:
        response = client.generate_presigned_post(Bucket = bucket_name,
                                                  Key = object_name,
                                                  ExpiresIn = expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response
