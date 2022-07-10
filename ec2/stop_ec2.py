import boto3
client = boto3.client('ec2')
client = boto3.client('ec2')
AWS_REGION = "ap-southeast-1"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)

INSTANCE_LIST =[
"i-xxxx"
                ]

for instance in INSTANCE_LIST :

    response = client.describe_tags(
        Filters=[{'Name': 'resource-id','Values': [instance]}])
    for i in response["Tags"] :
        tag_key = i["Key"]
        tag_value = i["Value"]
        if str(tag_key) == "Name" :
            instance_Name = tag_value
        
    # print(instance_Name)
    instance_operation = EC2_RESOURCE.Instance(instance)
    instance_operation.stop()
    print("Instance",instance_Name,"-->",instance,"stopping")
    instance_operation.wait_until_stopped()
    print("Instance",instance_Name,"-->",instance,"Finnally stopped")
    
    ec2 = boto3.resource('ec2')
    instance_var = ec2.Instance(instance)
    response = instance_var.describe_attribute(Attribute='blockDeviceMapping')
    data = response["BlockDeviceMappings"]
    # DeviceName = data["DeviceName"]
    # VolumeId = data["Ebs"]

    for each in data :
        DeviceName = each["DeviceName"]
        VolumeId = each["Ebs"]["VolumeId"]
        # print(DeviceName)
        # print(VolumeId)
        # print(instance)
        
    print("Instance :" ,instance_Name,"DeviceName",DeviceName,"| VolumeId - ",VolumeId,"will be Deattached")
    response = client.detach_volume(
        Device=DeviceName,
        # Force=True|False,
        InstanceId=instance,
        VolumeId=VolumeId,
        # DryRun=True
    )
    print("Instance :" ,instance_Name,"DeviceName",DeviceName,"| VolumeId - ",VolumeId,"has be Deattached")
