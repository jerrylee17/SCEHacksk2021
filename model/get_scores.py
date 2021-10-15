import json
import boto3


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket="sce-hacks-arson", Key="output.csv")
    content = {
        x.split(",")[0]: x.split(",")[1]
        for x in response["Body"].read().decode("utf-8").split()
    }
    return {"statusCode": 200, "body": content}
