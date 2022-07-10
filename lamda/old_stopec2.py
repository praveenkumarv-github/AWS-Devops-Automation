import boto3
region = 'ap-southeast-1'
instances = []
rdsInstances = []
def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    rds = boto3.client('rds', region_name=region)
    ec2.stop_instances(InstanceIds=instances)
    for i in rdsInstances: 
        print('Stoping RDS '+ i) 
        rds.stop_db_instance(DBInstanceIdentifier=i)
    print ('stopped your instances: ' + str(instances))
    print ('stopped your RDS instances: ' + str(rdsInstances))