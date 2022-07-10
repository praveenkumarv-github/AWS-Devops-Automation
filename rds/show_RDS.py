#db-instance-identifier
# describe_db_engine_versions

import boto3
db_list = []

client = boto3.client('rds')
# client = boto3.client('rds',region_name="ap-south-1")

count = 0 
response = client.describe_db_instances(
    # logGroupNamePrefix='Pro',
    # nextToken='string',
    # limit=123
)
# print(response)

raw_list = response['DBInstances']

for i in raw_list :
    count =  count +1
    db_list.append(i['DBInstanceIdentifier'])
# print("total number of Log Group : ",count)


for i in db_list :

    raw_data2 = client.describe_db_instances(DBInstanceIdentifier=i)
    # print(raw_data2) ##raw data of each
    lst_data2 = raw_data2['DBInstances']
    lst_data2 = lst_data2[0]

    data_DBInstanceIdentifier = lst_data2['DBInstanceIdentifier']
    data_DBInstanceClass = lst_data2['DBInstanceClass']
    data_Engine = lst_data2['Engine']
    data_MasterUsername = lst_data2['MasterUsername']
    data_AvailabilityZone = lst_data2['AvailabilityZone']
    data_AllocatedStorage = lst_data2['AllocatedStorage']
    data_EngineVersion = lst_data2['EngineVersion']
    data_MultiAZ = lst_data2['MultiAZ']
    data_Endpoint = lst_data2["Endpoint"]["Address"]
    data_VpcSecurityGroups = lst_data2['VpcSecurityGroups']
    data_VpcSecurityGroups = data_VpcSecurityGroups[0]
    data_DBInstanceArn = lst_data2["DBInstanceArn"]

    # data_EnabledCloudwatchLogsExports = lst_data2['EnabledCloudwatchLogsExports']
    # data_ReadReplicaDBInstanceIdentifiers = lst_data2['ReadReplicaDBInstanceIdentifiers']

    print(data_DBInstanceIdentifier , data_DBInstanceArn)
    # print()
    # print(data_DBInstanceClass)
    # print(data_Engine)
    # print(data_EngineVersion)
    # print(data_MasterUsername)
    # print(data_AvailabilityZone)
    # print(data_AllocatedStorage)
    # print(data_VpcSecurityGroups['VpcSecurityGroupId'])
    # print(data_EnabledCloudwatchLogsExports)
    # print("MultiAZ",data_MultiAZ)
    # print("##############################################")
    # print(data_Endpoint)
    # print(raw_list)
#MultiAZ