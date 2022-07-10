import boto3
from datetime import datetime,timedelta
import json
import http.client
result = []
rds_lst = []

# bytes pretty-printing
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]


def pretty_size(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')
for rds in rds_lst :
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'fetching_FreeStorageSpace',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/RDS',
                        'MetricName': 'FreeStorageSpace',
                        'Dimensions': [
                            {
                                "Name": "DBInstanceIdentifier",
                                "Value": rds
                            }
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Minimum'
                }
            }
        ],
        StartTime=(datetime.now() - timedelta(seconds=300 * 3)).timestamp(),
        EndTime=datetime.now().timestamp(),
        ScanBy='TimestampDescending')

    rdsSize = response['MetricDataResults'][0]['Values']
    if len(rdsSize) > 0 :
        rdsBytes = rdsSize[0]
        # print(rds,"-->",pretty_size(rdsBytes))
        data = rds,"-->",pretty_size(rdsBytes)
        result.append(data)
    else:
        print(rds, "is Down")
print ({' '.join([str(elem) for elem in result]) })
cos = ' '.join(map(str, result))
#Pushing message to slack block
conn = http.client.HTTPSConnection("hooks.slack.com")
payload = json.dumps({
"channel": "sre_test_logs",
"text": cos
})
headers = {
'Content-Type': 'application/json'
}
conn.request("POST", "<slackURL>", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


def lambda_handler(event, context):
    return 1