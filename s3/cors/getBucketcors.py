import boto3
import botocore
from bucketlist import *
client = boto3.client('s3')



for bucket in bukcetlst : 

    try:
        response = client.get_bucket_cors(Bucket=bucket)
        response_data = response["CORSRules"][0]
        # print(bucket , "-->" ,response_data)

    except botocore.exceptions.ClientError as error:
        # Put your error handling logic here
        if error.response['Error']['Code'] == 'NoSuchCORSConfiguration': 
            print(bucket,"-->","NoCORSConfiguration")
            pass
