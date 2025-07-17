# Data extraction using Amplitude Export API
# Documentation: https://amplitude.com/docs/apis/analytics/export

import requests
from dotenv import load_dotenv
load_dotenv()

def amp_ex(start_date, end_date, api_key, secret_key, output_file='data/data.zip'):
    """
    This function extracts data from AMplitude's Export API for a given date range and stores it in an output file, 'data.zip' by default.

    Args:
        start_date (str): Start date in format 'YYYYMMDDTHH' (e.g., 20241101T00)
        end_date (str): End date in format 'YYYYMMDDTHH' (e.g., 20241130T00)
        api_key (str) 
        secret_key (str)
        output_file (str)

    Output:
        bool: True if successful, False if not
    """

    url = f"https://analytics.eu.amplitude.com/api/2/export"

    parameters = {
        'start' : start_date, 
        'end' : end_date
    }

    # API call
    response = requests.get(
        url,
        auth=(api_key, secret_key),
        params=parameters
    )

    try:
        # Export the data as data.zip to the data folder if response was successful
        if response.status_code == 200:
            data = response.content
            print('Data retrieved successfully')

            # Save file
            with open(output_file, 'wb') as file:
                file.write(data)
            print(f'Data saved to {output_file}.')
        else:
            print(f"Error {response.status_code}: {response.text}")
        return True
    except requests.exceptions.RequestException as e:
        print(e)
    # Prints any custom exception
    # except Exception as e:
    #     print(e)
    # Prints whoops if raise_for_status wasn't 200
        return False
    except:
        print("Whoops!")
        return False