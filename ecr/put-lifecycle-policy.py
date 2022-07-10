import boto3

client = boto3.client('ecr')


response = client.put_lifecycle_policy(

    repositoryName='fmt-server',
    lifecyclePolicyText={
    "rules": [
        {
            "rulePriority": 1,
            "description": "Expire untagged images older than 90 days",
            "selection": {
                "tagStatus": "untagged",
                "countType": "sinceImagePushed",
                "countUnit": "days",
                "countNumber": 90
            },
            "action": {
                "type": "expire"
            }
        }
    ]
 }
)