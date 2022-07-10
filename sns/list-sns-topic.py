import boto3

client = boto3.client('sns')

lst_sns = []

for sns in lst_sns : 
    response = client.list_subscriptions_by_topic(
        TopicArn=sns,)
    for data in response["Subscriptions"]:
        # print(data)
        if "SubscriptionArn" :
            print(sns,"SubscriptionArn",data["SubscriptionArn"],"Protocol",data["Protocol"],"Endpoint",data["Endpoint"], "TopicArn",data["TopicArn"])


# response = client.list_topics()
# for data in response["Topics"] :
#     print(data)