import boto3

client = boto3.client('sqs')

# response = client.receive_message(
#     QueueUrl='wfmprod2-sp-to-wfm-errored',
#     MaxNumberOfMessages = 10
# )
# print(response)

paginator = client.get_paginator('list_queues')


response_iterator = paginator.paginate(
    QueueUrl='xx',
    PaginationConfig={
        'MaxItems': 123,
        'PageSize': 123,

    }
)

for i in response_iterator:
    print(i)


















# paginator = client.get_paginator('receive_message')


# # Create a PageIterator from the Paginator
# page_iterator = paginator.paginate(QueueUrl='wfmprod2-sp-to-wfm-errored')

# for page in page_iterator:
#     print(page)


# response = client.get_platform_application_attributes(
#     PlatformApplicationArn='string'
# )