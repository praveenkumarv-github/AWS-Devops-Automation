import boto3

client = boto3.client('ce')


response = client.get_cost_and_usage(
    TimePeriod = {
        'Start': '2022-07-08', #start of month
        'End': '2022-07-09' #end of next month
    },
    Granularity = 'DAILY',
    Metrics = ["UnblendedCost"],
    GroupBy = [
        {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
        },
        # {
        #     'Type': 'TAG',
        #     'Key': 'Name'
        # }
    ]
)
total = 0
# print(response["ResultsByTime"])

# for data in response["ResultsByTime"] :
#     for d in data["Groups"] :
#         print(d["Keys"][0],"-",d["Keys"][1]," $",d["Metrics"]["UnblendedCost"]["Amount"])
for data in response["ResultsByTime"] :
    for res in  data["Groups"] :
        service_name = res["Keys"][0]
        metrics = res["Metrics"]["UnblendedCost"]["Amount"]
        metrics=round(float(metrics),2)
        total = total + metrics
        print(service_name ,"-","$",metrics)

print("Total $",total)