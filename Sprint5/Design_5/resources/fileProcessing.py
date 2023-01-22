import boto3
import re
from collections import Counter
import os
import json

def lambda_handler(event, context):
    
    # Taking bucket name and key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    # Calling s3 client and taking object data by parsing bucket name and key, later reading and decoding the file data
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    client = boto3.client('s3')
    response = client.get_object(Bucket= bucket, Key=file_name)
    data = response['Body'].read().decode()

    # Removing non alphanumeric characters and adding each letter in list and counting the occurence of letters
    clean = re.sub(r'\W+', ' ', data)
    data_list = clean.split()
    count_data = Counter(data_list)

    print(count_data)

    # Calling output S3 bucket from environment variables and setting file name for our output file
    output_bucket = os.environ['S3OutputBucket']
    output_filename = "output_" + file_name

    # Converting our data to bytes 
    uploadByteStream = bytes(json.dumps(count_data).encode('UTF-8'))

    # Putting output file to our output bucket 
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
    client.put_object(Bucket=output_bucket, Key=output_filename, Body=uploadByteStream)

    print("uploaded output file to s3 bucket")
    return count_data