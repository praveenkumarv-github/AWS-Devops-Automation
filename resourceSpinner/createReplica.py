import boto3
import botocore.exceptions

rdsClient = boto3.client('rds')
ec2Client = boto3.client('ec2')


soure_RDS = "uat-atlas-enc22"
read_replica_name = "lamda-replica-testing" + "-" + soure_RDS
DBInstanceClass = "db.t3.small"

resultData = {}

def create_db_instance_read_replica(DBInstanceClass,soure_RDS,read_replica_name) :
    response = rdsClient.create_db_instance_read_replica(
        DBInstanceIdentifier=read_replica_name,
        SourceDBInstanceIdentifier=soure_RDS,
        DBInstanceClass=DBInstanceClass,
        AvailabilityZone=describe_AvailabilityZone(soure_RDS),
        Port=3306,
        MultiAZ=False,
        AutoMinorVersionUpgrade=True,
        PubliclyAccessible=False,
        Tags=[
            {
                'Key': 'CreatedBY',
                'Value': 'Praveen-SRE'
            },
            {
                'Key': 'CreatedFor',
                'Value': 'Testing'
            }
        ],
        VpcSecurityGroupIds=describe_VpcSecurityGroupIds(soure_RDS),
        StorageType='gp2',
        CopyTagsToSnapshot=True,
        EnableIAMDatabaseAuthentication=True)
    return response

def describe_db_instances(dataBaseName) :
    try :
        response = rdsClient.describe_db_instances(DBInstanceIdentifier=dataBaseName)
        return response
    except botocore.errorfactory.ClientError as error:
        if error.response['Error']['Code'] == 'DBInstanceNotFound':
            print(error.response['Error']['Code'] , dataBaseName)
            exit()
        else :
            print(error.response['Error']['Message'])
            exit()

def describe_VpcSecurityGroupIds (dataBaseName):
    status_soure_RDS = describe_db_instances(dataBaseName)
    VpcSecurityGroups = status_soure_RDS["DBInstances"][0]["VpcSecurityGroups"]
    VpcSecurityGroupIds = [VpcSecurityGroupIds["VpcSecurityGroupId"] for VpcSecurityGroupIds in VpcSecurityGroups]
    return VpcSecurityGroupIds

def describe_AvailabilityZone(dataBaseName):
    status_soure_RDS = describe_db_instances(dataBaseName)
    AvailabilityZone = status_soure_RDS["DBInstances"][0]["AvailabilityZone"]
    return AvailabilityZone

print(describe_VpcSecurityGroupIds(soure_RDS))
print(describe_AvailabilityZone(soure_RDS))

def ReplicaCreation(DBInstanceClass,soure_RDS,read_replica_name) :
    try :
        replicaCreation_data = create_db_instance_read_replica(DBInstanceClass,soure_RDS,read_replica_name)
        print(replicaCreation_data["DBInstance"])
    except botocore.errorfactory.ClientError as error:
        if error.response['Error']['Code'] == 'DBInstanceAlreadyExists':
            print(error.response['Error']['Message'],read_replica_name)
        else :
            print(error.response['Error']['Message'])

ReplicaCreation(DBInstanceClass,soure_RDS,read_replica_name)
print(resultData)