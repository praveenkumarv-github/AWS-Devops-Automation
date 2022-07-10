import boto3
import botocore.exceptions
import http.client
import json
from datetime import date, timedelta

client = boto3.client('ec2')

clientec2_Singapore = boto3.client('ec2',region_name='ap-southeast-1') #Asia Pacific (Singapore)
clientrds_Singapore = boto3.client('rds',region_name='ap-southeast-1') #Asia Pacific (Singapore)
ec2Instances_Singapore =[]
rdsInstances_Singapore = []


result_data= []
metadata = '''This is auto-generated LAMDA Function 
on : ''' + date.today().strftime("%d-%b-%Y") +'''

'''
result_data.append(metadata)

def get_instanceName(instanceid,client_region):
    response = client_region.describe_tags(
        Filters=[{'Name': 'resource-id','Values': [instanceid]}])
    for i in response["Tags"] :
        tag_key = i["Key"]
        tag_value = i["Value"]
        if str(tag_key) == "Name" :
            return tag_value
def stopEc2instance(instanceid,client_region):
    response = client_region.stop_instances(InstanceIds=[instanceid])
def statusChecker(state,instance_identification_Name):
    if state == 0 :
        state_res=instance_identification_Name+" instance is pending"
        return state_res
    if state == 16:
        state_res=instance_identification_Name+" instance is already running"
        return state_res
    if state == 32 :
        state_res=instance_identification_Name+" instance is shutting-down"
        return state_res
    if state == 48 :
        state_res=instance_identification_Name+" instance is terminated"
        return state_res
    if state == 64 :
        state_res=instance_identification_Name+" instance is stopping"
        return state_res
    if state == 80 :
        state_res=instance_identification_Name+" instance is stopped"
        return state_res

#EC2 block
def stoptEC2(ec2Instances,client_region) : 
    for instance in ec2Instances :
        try :
            instance_identification_Name=get_instanceName(instance,client_region)
            response = client_region.describe_instance_status(InstanceIds=[instance])
            if len(response["InstanceStatuses"] ) <= 1 :
                stopEc2instance(instance,client_region) #ec2.stop
                state_res = instance_identification_Name+" is Stopped"
                result_data.append(state_res)
            else :
                state = response["InstanceStatuses"][0]["InstanceState"]["Code"]
                state_res = statusChecker(state,instance_identification_Name)
                result_data.append(state_res) #collecting output for slack
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'InvalidInstanceID.Malformed': 
                result_data.append(instance+" EC2 not exist")

#RDS block
def stopRDS(rdsInstances,clientrds) : 
    for rds in rdsInstances : 
        try :
            rds_response = clientrds.describe_db_instances(DBInstanceIdentifier=rds) #get Status before stooping
            DBInstanceStatus = (rds_response["DBInstances"][0]["DBInstanceStatus"])
            pre_DBInstanceStatus = rds + " is " + DBInstanceStatus
            result_data.append(pre_DBInstanceStatus)
            print(str(pre_DBInstanceStatus))
            if str(DBInstanceStatus) == "available" :
                start_rds_response = clientrds.stop_db_instance(DBInstanceIdentifier=rds)  #RDS.instance.stop

                rds_response = clientrds.describe_db_instances(DBInstanceIdentifier=rds) #get Status after stooping
                DBInstanceStatus = (rds_response["DBInstances"][0]["DBInstanceStatus"])
                post_DBInstanceStatus = rds + " is " + DBInstanceStatus
                result_data.append(post_DBInstanceStatus)

        except botocore.errorfactory.ClientError as error:
            if error.response['Error']['Code'] == 'InvalidDBInstanceState':
                if str(DBInstanceStatus) == "available" :
                    exception_state = rds + " AlreadyRunning"
                    result_data.append(exception_state)
            else:
                exception_state = rds +" "+ error.response['Error']['Code']
                result_data.append(exception_state)

stoptEC2(ec2Instances_Singapore,clientec2_Singapore)
stopRDS(rdsInstances_Singapore,clientrds_Singapore)

#Pushing message to slack block
conn = http.client.HTTPSConnection("hooks.slack.com")
for data in result_data :
    payload = json.dumps({"channel": "sre_test_logs","text": data})
    headers = {'Content-Type': 'application/json'}
    conn.request("POST", "<slackURL>", payload, headers)
    res = conn.getresponse()
    data = res.read()
print(data.decode("utf-8"))

def lambda_handler(event, context):
    return 1