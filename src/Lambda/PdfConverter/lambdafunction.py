

import json
from converter import pdf_to_text
import tempfile
import csv
import boto3

def lambda_handler(event, context):

    inputbucket = "yourinputbucket"
    destbucket = "youroutputbucket"

    #send name of file to pdf_to_text to be converted
    pdfname =  event["Records"][0]["s3"]["object"]["key"][:-4]
    text = pdf_to_text(pdfname + ".pdf", 'inputbucket')



    #save to temp
    with open('/tmp/pdftexts.txt', 'w') as myfile:
        myfile.write(text)

    #upload to s3
    s3_client = boto3.client('s3')
    s3_client.upload_file('/tmp/pdftexts.txt', destbucket, pdfname + ".txt")



    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
