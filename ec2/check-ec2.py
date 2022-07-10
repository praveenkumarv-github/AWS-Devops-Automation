import boto3
# id = "i-07336ac1268386a46"
instanceID = 'i-xxx'
client = boto3.client('ec2')

def get_instanceName(instanceID):
    response = client.describe_tags(
        Filters=[{'Name': 'resource-id','Values': [instanceID]}])
    for i in response["Tags"] :
        tag_key = i["Key"]
        tag_value = i["Value"]
        if str(tag_key) == "Name" :
            return tag_value
response = client.describe_instances(InstanceIds=[instanceID])


InstanceType = response["Reservations"][0]["Instances"][0]["InstanceType"]
InstanceState = response["Reservations"][0]["Instances"][0]["State"]["Name"]
InstanceName = get_instanceName(instanceID)

print("InstanceName :",InstanceName)
print("InstanceType :",InstanceType)
print("InstanceState :",InstanceState)


# Stop the instance
client.stop_instances(InstanceIds=[instanceID])
waiter=client.get_waiter('instance_stopped')
waiter.wait(InstanceIds=[instanceID])

# Change the instance type
client.modify_instance_attribute(InstanceId=instanceID, Attribute='instanceType', Value='t3.xlarge')

# Start the instance
client.start_instances(InstanceIds=[instanceID])

