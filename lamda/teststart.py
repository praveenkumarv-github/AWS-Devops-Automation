import boto3
import botocore.exceptions
import http.client
import json
from datetime import date, timedelta

ec2Instances_Singapore =[]  


clientec2_Singapore = boto3.client('ec2',region_name='ap-southeast-1') #Asia Pacific (Singapore)

def get_instanceName(instanceid,client_region):
    response = client_region.describe_tags(
        Filters=[{'Name': 'resource-id','Values': [instanceid]}])
    for i in response["Tags"] :
        tag_key = i["Key"]
        tag_value = i["Value"]
        if str(tag_key) == "Name" :
            return tag_value

for i in ec2Instances_Singapore :
    print(get_instanceName(i,clientec2_Singapore))

def lambda_handler(event, context):
    return 1