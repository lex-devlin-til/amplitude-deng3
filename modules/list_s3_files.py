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

# Define list of all files in s3 bucket/folder (for testing)
s3_folder_files = list_s3_files(aws_access_key, aws_secret_key, bucket, bucket_folder)

# Max hour function for getting the greatest hour currently in the data
def get_max_hour(filenames):

# Grab datetime portion of filename, take the max
    files_with_timestamps = []
    for filename in filenames:

        # If it's json, split it. Date = stuff after _, before #. The 'parts' business is what works, doing it all in one line doesn't work.
        if filename[-5:] == '.json':
            parts = filename.split('_', 1)
            filedate = parts[1].split('#')[0] if len(parts) > 1 else ""
            parsed_date = datetime.datetime.strptime(filedate, "%Y-%m-%d_%H")
            files_with_timestamps.append(parsed_date)

    # Returns a list of tuples, each containing a filename and its parsed date
    # Max can be taken from this later.
    max_date = max(files_with_timestamps)
    return max_date

# for testing
# var = s3_max_hour(s3_folder_files)
# print(var)

