import boto3
region = 'ap-southeast-1'
instances = []
rdsInstances = []
def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=instances)
    rds = boto3.client('rds', region_name=region)
    for i in rdsInstances: 
        print('Starting RDS '+ i) 
        rds.start_db_instance(DBInstanceIdentifier=i)
    print ('started your instances: ' + str(instances))
    print ('started your RDS instances: ' + str(rdsInstances)) 