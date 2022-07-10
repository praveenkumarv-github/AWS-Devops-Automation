import boto3

client = boto3.client('sns',region_name='ap-south-1')

response = client.create_topic(
    Name='Prod_RDS_instance_alerts',)

print(response)