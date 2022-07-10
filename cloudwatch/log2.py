import boto3

client = boto3.client('cloudwatch')
paginator = client.get_paginator('describe_alarms')

response_iterator = paginator.paginate(
 
)
for data in response_iterator:
    print(data)
# for data in response_iterator["MetricAlarms"] :
#     print(data)
    