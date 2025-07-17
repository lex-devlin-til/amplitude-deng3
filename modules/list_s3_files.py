import boto3
import os
from dotenv import load_dotenv
import datetime

# Load .env
load_dotenv()

# Get keys etc from .env
aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')
bucket_folder = 'python-import/'

def list_s3_files(aws_access_key, aws_secret_key, bucket, bucket_folder):

    # Create S3 Client using AWS creds
    s3_client = boto3.client(
        's3',
        aws_access_key_id = aws_access_key,
        aws_secret_access_key = aws_secret_key
    )

    # Create list of all S3 files in bucket/bucket_folder
    s3_folder_files = []
    response = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix=bucket_folder)
    for obj in response.get('Contents', []):
        s3_folder_files.append(obj['Key'])

    # return(response)
    return(s3_folder_files)

s3_folder_files = list_s3_files(aws_access_key, aws_secret_key, bucket, bucket_folder)

def s3_max_hour(s3_folder_files):

# Grab datetime portion of filename, take the max
    datetime_list = []
    for filename in s3_folder_files: #s3_folder_files:
        if filename[-5:] == '.json':
            datetime_list.append(filename[filename.find('_') + 1:][:-7])
    return datetime_list
        
var = s3_max_hour(s3_folder_files)
print(var)

# datetime.datetime(2025, 7, 16, 8, 32, 11, tzinfo=tzutc())