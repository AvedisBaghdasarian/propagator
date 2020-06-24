import json
import boto3
import botocore
import tarfile

from io import BytesIO
s3_client = boto3.client('s3')

def lambda_handler(event, context):

    inputbucket = "yourinputbucket"
    destbucket = "yourdestbucket"

    key = event['Records'][0]['s3']['object']['key']

    #gets tar file from s3
    input_tar_file = s3_client.get_object(Bucket = inputbucket, Key = key)
    input_tar_content = input_tar_file['Body'].read()

    #open file in memory to avoid storage constraints
    with tarfile.open(fileobj = BytesIO(input_tar_content)) as tar:
        for tar_resource in tar:
            if (tar_resource.isfile()):
                #extract and reupload to s3
                inner_file_bytes = tar.extractfile(tar_resource).read()
                s3_client.upload_fileobj(BytesIO(inner_file_bytes), Bucket = destbucket, Key = (tar_resource.name))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
