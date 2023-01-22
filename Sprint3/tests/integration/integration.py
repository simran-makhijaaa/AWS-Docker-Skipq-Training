import boto3

# Integration test

def integ_test():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-2")

    try:
        table = dynamodb.Table("Beta-SimranStage-APIUrlTableE6022B99-1MFX4W87B272V")
        response = table.scan()
        data = response["Items"]

        print(response)
        print(data)
        return data
    except Exception as e:
        print("An Error occured :", e)
        raise


integ_test()