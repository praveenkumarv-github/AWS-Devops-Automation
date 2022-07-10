group_name = 'group_namen'
import boto3, json, time
client = boto3.client('logs')
all_streams = []

stream_batch = client.describe_log_streams(logGroupName=group_name)
all_streams += stream_batch['logStreams']
while 'nextToken' in stream_batch:
	stream_batch = client.describe_log_streams(logGroupName=group_name,nextToken=stream_batch['nextToken'])
	all_streams += stream_batch['logStreams']
	print(len(all_streams))

stream_names = [stream['logStreamName'] for stream in all_streams]
out_to = ''
with open("cloud_logs.txt", 'a') as out_to :
    for stream in stream_names:
        logs_batch = client.get_log_events(logGroupName=group_name, logStreamName=stream,startTime=1640995200000,endTime=1651363200000)
        for event in logs_batch['events']:
            event.update({'group': group_name, 'stream':stream })
            out_to.write(json.dumps(event) + '\n')
        print(stream, ":", len(logs_batch['events']))
        while 'nextToken' in logs_batch:
                logs_batch = client.get_log_events(logGroupName=group_name, logStreamName=stream, nextToken=logs_batch['nextToken'],startTime=1640995200000,endTime=1651363200000)
                for event in logs_batch['events']:
                    event.update({'group': group_name, 'stream':stream })
                    out_to.write(json.dumps(event) + '\n')




