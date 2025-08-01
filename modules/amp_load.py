import boto3
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Get keys etc from .env
aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')
bucket_folder = 'python-import/'

def amp_load(aws_access_key, aws_secret_key, bucket, bucket_folder):

# Create S3 Client using AWS creds
    s3_client = boto3.client(
        's3',
        aws_access_key_id = aws_access_key,
        aws_secret_access_key = aws_secret_key
    )

    # Loop through filenames in data folder
    data_folder = 'data'
    datafiles = os.listdir(data_folder)
    upload_count = 0
    error_count = 0
    for filename in datafiles:
        if filename[-5:] == '.json':
            local_file_location = data_folder + '/' + filename
            aws_file_destination = bucket_folder + filename

            # Upload files to S3 bucket, count number of uploads, error handle
            try:
                s3_client.upload_file(local_file_location, bucket, aws_file_destination)
                upload_count += 1
                try:
                    os.remove(local_file_location)
                except:
                    print(f'File {filename} was uploaded to S3, but did not get deleted from local folder.')
                    error_count += 1
            except:
                print(f'File {filename} not uploaded.')
                error_count += 1

    # Success/error messages   
    print(f'{upload_count} json files uploaded to S3.')
    if error_count > 0:
        print(f'{error_count} json files failed to upload.')