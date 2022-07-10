import boto3

client = boto3.client('sqs')
count = 0
lst = [
    ""]


for i in lst :
    response = client.list_queues(
        QueueNamePrefix=i,
    )
    data = response["QueueUrls"]
    for d in data :
        count = count +1 
        print(d)
print(count)