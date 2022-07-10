import boto3
import json

region_name = 'ap-southeast-1'
queue_name = "ququeName"
counter = 0
max_queue_messages = 10
message_bodies = []
sqs = boto3.resource('sqs', region_name=region_name)
queue = sqs.get_queue_by_name(QueueName=queue_name)
while True:
    # messages_to_delete = []
    for message in queue.receive_messages(
            MaxNumberOfMessages=max_queue_messages):
        counter =  counter + 1
        # process message body
        
        body = json.loads(message.body)
        print(body)
        message_bodies.append(body)
        # add message to delete
        # messages_to_delete.append({
        #     'Id': message.message_id,
        #     'ReceiptHandle': message.receipt_handle
        # })
    if counter == 9:
        break
    # # if you don't receive any notifications the
    # # messages_to_delete list will be empty
    # if len(messages_to_delete) == 0:
    #     break
    # # delete messages to remove them from SQS queue
    # # handle any errors
    # else:
    #     delete_response = queue.delete_messages(
    #             Entries=messages_to_delete)

# print(message_bodies)