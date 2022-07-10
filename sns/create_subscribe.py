import boto3


list = ["xxx"]
client = boto3.client('sns',region_name='ap-south-1')

for ele in list:
    response = client.subscribe(
        TopicArn='arn:aws:sns:ap-south-1:609249146283:Prod_RDS_instance_alerts',
        Protocol='sms',
        Endpoint= ele,
        ReturnSubscriptionArn=True
    )

print(response)


