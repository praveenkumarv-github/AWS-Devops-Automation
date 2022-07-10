import boto3
from datetime import date ,datetime, timezone
import datetime

today = datetime.datetime.now(timezone.utc)
print(type(today),today)

client = boto3.client('iam')

response = client.list_access_keys(
    UserName='kishore')

# print(response)

for data in response["AccessKeyMetadata"]:
    AccessKeyId = data["AccessKeyId"]
    CreateDate = data["CreateDate"]
    print(type(today),CreateDate)
    dif = today - CreateDate
    print(dif)
    




