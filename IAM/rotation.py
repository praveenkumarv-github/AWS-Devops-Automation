import boto3
from botocore.exceptions import ClientError
import datetime
import json
import http.client

keyRotation_users = []
alluser_secret_data  = []
iam_client = boto3.client('iam')


user_lst_response = iam_client.list_users()
for data in user_lst_response["Users"]:
    username = data["UserName"]
    tag_response = iam_client.list_user_tags(UserName=username)
    tag_data = tag_response["Tags"]
    if len(tag_data) > 0:
        for tag in tag_data :
            if tag["Key"] == "PRAVEEN":
                # usermailid = tag["Value"]
                keyRotation_users.append(username)

def list_access_key(user, days_filter, status_filter):
    keydetails=iam_client.list_access_keys(UserName=user)
    key_details={}
    user_iam_details=[]
    
    # Some user may have 2 access keys.
    for keys in keydetails['AccessKeyMetadata']:
        if (days:=time_diff(keys['CreateDate'])) >= days_filter and keys['Status']==status_filter:
            key_details['UserName']=keys['UserName']
            key_details['AccessKeyId']=keys['AccessKeyId']
            key_details['days']=days
            key_details['status']=keys['Status']
            user_iam_details.append(key_details)
            key_details={}
    
    return user_iam_details

def time_diff(keycreatedtime):
    now=datetime.datetime.now(datetime.timezone.utc)
    diff=now-keycreatedtime
    return diff.days
def create_key(username):
    try :
        access_key_metadata = iam_client.create_access_key(UserName=username)
        access_key = access_key_metadata['AccessKey']['AccessKeyId']
        secret_key = access_key_metadata['AccessKey']['SecretAccessKey']
        secret_data = username , access_key , secret_key
        alluser_secret_data.append(secret_data)
    except ClientError as e:
        user_iam_details=iam_client.list_access_keys(UserName=user)
        print("Threre is total AccessKeys: 2 for ", username)
        print(user_iam_details)
def disable_key(access_key, username):
    try:
        iam_client.update_access_key(UserName=username, AccessKeyId=access_key, Status="Inactive")
        print(access_key + " has been disabled.")
    except ClientError as e:
        print("The access key with id %s cannot be found" % access_key)
def delete_key(access_key, username):
    try:
        iam_client.delete_access_key(UserName=username, AccessKeyId=access_key)
        print (access_key + " has been deleted.")
    except ClientError as e:
        print("The access key with id %s cannot be found" % access_key)

# def lambda_handler(event, context):

for user in keyRotation_users : 
    user_iam_details=list_access_key(user=user,days_filter=80,status_filter='Active')
    for _ in user_iam_details:
        print(_)
        # disable_key(access_key=_['AccessKeyId'], username=_['UserName'])
        # delete_key(access_key=_['AccessKeyId'], username=_['UserName'])
        secret_data = create_key(username=_['UserName'])
    
    for user_secret_data in alluser_secret_data :
        for cos in user_secret_data :
            print(cos)
    # cos = alluser_secret_data
    #Pushing message to slack block
            conn = http.client.HTTPSConnection("hooks.slack.com")
            payload = json.dumps({
            "channel": "sre_test_logs",
            "text": cos
            })
            headers = {
            'Content-Type': 'application/json'
            }
            conn.request("POST", "<SLACK_URL>", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))        

    # return {
    #     'statusCode': 200,
    #     'body': list_access_key(user=user,days_filter=0,status_filter='Active')
    # }