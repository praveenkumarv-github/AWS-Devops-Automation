import logging
import boto3
from botocore.exceptions import ClientError


# Retrieve the list of existing buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names

for bucket in response['Buckets']:
    print(bucket["Name"])