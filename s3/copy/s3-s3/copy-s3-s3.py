import boto3
from echoFile import *
with open('result.log', 'w') as f:

    for echo in echoLst:
        old_bucket_name = 'sourcebucket'
        old_prefix = echo
        new_bucket_name = 'des
        new_prefix = echo
        s3 = boto3.resource('s3')
        old_bucket = s3.Bucket(old_bucket_name)
        new_bucket = s3.Bucket(new_bucket_name)

        for obj in old_bucket.objects.filter(Prefix=old_prefix):
            old_source = { 'Bucket': old_bucket_name,
                        'Key': obj.key}
            # replace the prefix
            new_key = obj.key.replace(old_prefix, new_prefix, 1)
            new_obj = new_bucket.Object(new_key)
            new_obj.copy(old_source)
            print(echo,"->",new_key)
            write_data =new_key
            f.write(new_key)
            f.write('\n')