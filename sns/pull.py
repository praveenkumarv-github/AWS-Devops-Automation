import boto3

# Create SQS client
sqs = boto3.client('sqs')

response = sqs.receive_message(
    QueueUrl='wfmprod2-sema-generation-errored',
    MaxNumberOfMessages=22,

)

print(response)