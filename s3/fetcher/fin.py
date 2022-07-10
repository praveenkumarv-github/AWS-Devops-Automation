from fileinput import filename
import boto3
import botocore

# BUCKET_NAME = 'bkp-prod-cloud-src/raw-files/' # replace with your bucket name

BUCKET_NAME = "prod-cog-tricog" # replace with your bucket name
# KEY = 'my_image_in_s3.jpg' # replace with your object key
objects = [""]
s3 = boto3.resource('s3')

for obj in objects :
    try:
        pathname = "/home/praveen/Downloads/" + obj 
        s3.Bucket(BUCKET_NAME).download_file(obj, pathname)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(obj ,"  -->" , "The object does not exist.")
        else:
            raise
