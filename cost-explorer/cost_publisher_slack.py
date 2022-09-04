import http.client
import json
from datetime import date, timedelta
import boto3
import datetime

cost_Book = []

client = boto3.client('ce')


###########3
res_get_cost_and_usage = client.get_cost_and_usage(
    TimePeriod = {
        'Start': '2022-05-01', #start of month
        'End': '2022-06-01' #start of next month
    },
    Granularity = 'MONTHLY',
    Metrics = ["UnblendedCost"],
    GroupBy = [
        {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
        },])
totalcost = 0
for data in res_get_cost_and_usage["ResultsByTime"] :
    for res in  data["Groups"] :
        service_name = res["Keys"][0]
        metrics = res["Metrics"]["UnblendedCost"]["Amount"]
        metrics=round(float(metrics),2)
        totalcost = totalcost + metrics
        print(service_name ,"-","$",metrics)
print("Total $",totalcost)
############4


def getcost_by_daterange(start_date,end_date) :
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=[
            'UnblendedCost',
        ],
    )
    data = (response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
    return round(float(data),2)

#previous_Month
start_day_of_cuurent_month = date.today().replace(day=1) 
last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
start_day_of_prev_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)
# print(start_day_of_prev_month,"-",start_day_of_cuurent_month)
# print(getcost_by_daterange(str(start_day_of_prev_month),str(start_day_of_cuurent_month)))
descp = "Previous Month Cost $"
previous_month =getcost_by_daterange(str(start_day_of_prev_month),str(start_day_of_cuurent_month))
previous_month = descp + str(previous_month)
# currentMonth_cost

today_date = date.today()
# print(getcost_by_daterange(str(start_day_of_cuurent_month),str(today_date)))

descp = "Current Month Cost $"
if start_day_of_cuurent_month == today_date :
    currentMonth_cost= "Current Month Cost $ Month Started Today"
else :
    currentMonth_cost = getcost_by_daterange(str(start_day_of_cuurent_month),str(today_date))
    print("asdfasjasdf",str(start_day_of_cuurent_month),str(today_date))
    currentMonth_cost = descp + str(currentMonth_cost)

x = datetime.datetime.now()
today = x.strftime("%F")
# print(today)
tommorow = datetime.date.today() + datetime.timedelta(days=1)
# print(tommorow)

#Daly Forcast average Value
response = client.get_cost_forecast(
    TimePeriod={
        'Start': str(today),
        'End': str(tommorow)
    },
    Metric='UNBLENDED_COST', ##Unblended costs represent your usage costs on the day they are charged to you
    Granularity='DAILY',
)
daily_data = response['Total']
descp = "Daily Forecast Cost $"
daily_cost = str(round(float(daily_data['Amount']),2))
daily_cost = descp + daily_cost

#MONTHLY Forcast
response = client.get_cost_forecast(
    TimePeriod={
        'Start': str(today),
        'End': str(tommorow)
    },
    Metric='UNBLENDED_COST', #Unblended costs represent your usage costs on the day they are charged to you
    Granularity='MONTHLY',
)
monthly_data = response['Total']
descp = "MONTHLY Forecast Cost $"
monthly_cost =round(float(monthly_data['Amount']),2)
monthly_cost = descp + str(monthly_cost)

#this block is not requreid , hust created for debugging
cost_Book.append("This is auto-generated from AWS LAMDA As on :")
cost_Book.append(today_date.strftime("%d-%b-%Y"))
cost_Book.append(previous_month)
cost_Book.append(currentMonth_cost)
cost_Book.append(daily_cost)
cost_Book.append(monthly_cost)
cost_Book.append("###############")

#output Var
cos = "This is auto-generated from AWS LAMDA  :" + "\n" + today_date.strftime("%d-%b-%Y")  + "\n" +  previous_month + "\n" + currentMonth_cost + "\n" + daily_cost + "\n" + monthly_cost
print(cos)

#Pushing message to slack block
conn = http.client.HTTPSConnection("hooks.slack.com")
payload = json.dumps({
"channel": "sre_test_logs",
"text": cos
})
headers = {
'Content-Type': 'application/json'
}
conn.request("POST", "<Slackwebhooks>", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


def lambda_handler(event, context):
    return 1