import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from modules.extract_amplitude_files import amp_ex
from modules.unzip_json import unzip_json
from modules.list_s3_files import list_s3_files
from modules.list_s3_files import s3_max_hour


# Load .env
load_dotenv()

# Get keys from .env file
api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")
aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')
bucket_folder = 'python-import/'

# Define variables
# prev_day = datetime.now() - timedelta(days=1)
# start_date = prev_day.strftime('%Y%m%dT00')
# end_date = datetime.now().strftime('%Y%m%dT23')

# Create list of existing files in lex-amp-deng3/python-import/ folder
s3_files = list_s3_files(aws_access_key, aws_secret_key, bucket, bucket_folder)

# Define date variables according to what the latest date/hour in the existing s3 data is
start_timestamp = s3_max_hour(s3_files) + timedelta(hours=1)
start_datetime = start_timestamp.strftime('%Y%m%dT00')
end_datetime = datetime.now().strftime('%Y%m%dT%h')



# Run amp_ex to call Amplitude API
amp_ex(start_datetime, end_datetime, api_key, secret_key)

# Unzip the jsons out of the gzip nonsense. Can specify zip name and data directory as args, defaults are 'data.zip' and 'data'
unzip_json()