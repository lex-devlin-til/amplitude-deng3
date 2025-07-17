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

# Create S3 Client using AWS creds
s3_client = boto3.client(
    's3',
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_key
)

aws_folder_files = []
response = s3_client.list_objects_v2(
    Bucket=bucket,
    Prefix=bucket_folder)
for obj in response.get('Contents', []):
    aws_folder_files.append(obj['Key'])
print(aws_folder_files)

# Set file start and end points
# data_folder = "data"
# aws_file_destination = "python-import/test_file.json"

# Loop through filenames in data folder
# datafiles = os.listdir(data_folder)
# upload_count = 0
# error_count = 0
# for filename in datafiles:
#     if filename[-5:] == '.json':
#         local_file_location = data_folder + '/' + filename
#         aws_file_destination = 'python-import' + '/' + filename
#         try:
#             s3_client.upload_file(local_file_location, bucket, aws_file_destination)
#             upload_count += 1
#         except:
#             print(f'File {filename} not uploaded')
# print(f'{upload_count} json files uploaded to S3.')
# if error_count > 0:
#     print(f'{error_count} json files failed to upload.')

# Upload file to s3 bucket






