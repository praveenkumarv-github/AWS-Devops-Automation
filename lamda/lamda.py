import boto3

client = boto3.client('lambda',region_name='us-east-1')

response = client.list_functions()

for data in response :
    for data1 in response["Functions"] :
        if "Runtime" in data1 :
            print(data1["FunctionName"],"--->",data1["Runtime"])


