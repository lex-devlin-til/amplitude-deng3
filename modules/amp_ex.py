# Data extraction using Amplitude Export API
# Documentation: https://amplitude.com/docs/apis/analytics/export

import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
import zipfile
import gzip
import shutil
import tempfile
import time

# Load .env
load_dotenv()

# Define variables
prev_day = datetime.now() - timedelta(days=1)
starttime = prev_day.strftime('%Y%m%dT00')
endtime = datetime.now().strftime('%Y%m%dT23')
starttime = '20250705T00'
endtime = '20250710T23'

api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")

url = f"https://analytics.eu.amplitude.com/api/2/export"

def amp_ex(starttime, endtime, api_key, secret_key):
    
    parameters = {
        'start' : starttime,
        'end' : endtime
    }

    # API call
    response = requests.get(
        url,
        auth=(api_key, secret_key),
        params=parameters
    )

    current_try = 0
    wait_time = 2 # seconds
    while current_try < 5:
        try:
            # Export the data as data.zip to the data folder
            if response.status_code == 200:
                data = response.content
                print('Data retrieved successfully')
                with open("data/data.zip", 'wb') as file:
                    file.write(data)
            else:
                print('lol m8')
                print(f"Error {response.status_code}: {response.text}")

            # Make temporary directory for extraction. Space for intermediate processing that goes away afterward.
            temp_dir = tempfile.mkdtemp()

            # Create local output directory. Jsons go here.
            data_dir = "data"
            os.makedirs(data_dir, exist_ok=True)

            # Unpack gzip and put it in temp_dir. It should contain a single numerically named folder.
            with zipfile.ZipFile("data/data.zip", "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            # Get the text of the numerically named folder, which contains the gzips for each hour
            numerical_folder = next(f for f in os.listdir(temp_dir) if f.isdigit()) # python magic, Will S original version

            # folderlist = [] # alt version 1 per Jeff
            # for f in os.listdir(temp_dir):
            #     if f.isdigit():
            #         folderlist.append(f)
            # numerical_folder = emptylist[0]

            # numerical_folder = os.listdir(temp_dir)[0] # alt version 2 per Jeff

            # day_path = filepath of temp_directory concatenated with numerical_folder name
            numerical_folder_path = os.path.join(temp_dir, numerical_folder) 

            # Triple unpacking jsons, write the 
            for dirpath, dirnames, filenames in os.walk(numerical_folder_path): # os.walk() yields a 3-tuple
                for filename in filenames:
                    if filename.endswith('.gz'):
                        gz_path = os.path.join(dirpath, filename)
                        json_filename = filename[:-3] # All characters of filename except for the last three
                        output_path = os.path.join(data_dir, json_filename) # filepath = data folder 
                        with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                            shutil.copyfileobj(gz_file, out_file) # copying one file to the other location
            # putting gzip in final location?
        # if something went wrong with the request itself, print that error
            break
        except requests.exceptions.RequestException as e:
            print(e)
        # Prints any custom exception
        # except Exception as e:
        #     print(e)
        # Prints whoops if raise_for_status wasn't 200
        except:
            print("Whoops!")

        # adds 1 to current_try, waits to try again
        current_try += 1
        print('Attempt ')
        print(f'waiting, will try again in {wait_time} seconds...')
        time.sleep(wait_time)

    # prints a message if we tried too many times
    if current_try == 5:
        print('Too many tries. :(')