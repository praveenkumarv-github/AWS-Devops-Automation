import boto3

s3 = boto3.client('s3')
response = s3.list_buckets()

bucketname_lst = []

# Retrieve the list of existing buckets
for bucket in response['Buckets']:
    bucket = (bucket["Name"])
    # if bucket.startswith("uat") :
    bucketname_lst.append(bucket)
        # print(bucket)

for bucket in bucketname_lst:
    response = s3.list_bucket_intelligent_tiering_configurations(
        Bucket=bucket,
    )
    if "IntelligentTieringConfigurationList" in response:
        if response["IntelligentTieringConfigurationList"][0]["Status"] == "Enabled":
            print("Intelligent Tiering is Enabled on",bucket)
    else :
        # print("Not Found IntelligentTieringConfiguration on ",bucket)
        response = s3.put_bucket_intelligent_tiering_configuration(
            Bucket=bucket,
            Id='itc-boto',
            IntelligentTieringConfiguration={
                'Id': 'itc-boto',
                'Status': 'Enabled',
                "Tierings": [
                    {
                        "Days": 180,
                        "AccessTier": "DEEP_ARCHIVE_ACCESS"
                    },
                    {
                        "Days": 90,
                        "AccessTier": "ARCHIVE_ACCESS"
                    }
                ]
            }
        )
        # print("Enabled IntelligentTieringConfiguration on ",bucket)
        print("Enabling IntelligentTiering on ",bucket,"-->",response)












