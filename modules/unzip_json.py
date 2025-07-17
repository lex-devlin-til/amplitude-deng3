import os

def unzip_json(zip_name='data.zip', data_dir='data'):
    """
    Function that unzips the jsons out of the nightmare gzip jungle that came from the Amplitude API.

    """
    # Import libraries
    import zipfile
    import gzip
    import shutil
    import tempfile

    if not os.path.exists(os.path.join(data_dir, zip_name)):
        raise FileNotFoundError(f'Zip file not found in {data_dir}.')

    # Make temporary directory for extraction. Space for intermediate processing that goes away afterward.
    temp_dir = tempfile.mkdtemp()

    # Create local output directory. Jsons go here.
    os.makedirs(data_dir, exist_ok=True)

    # Unpack gzip and put it in temp_dir. It should contain a single numerically named folder.
    with zipfile.ZipFile(os.path.join(data_dir, zip_name), "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    # Get the text of the numerically named folder, which contains the gzips for each hour
    try:
        numerical_folder = next(f for f in os.listdir(temp_dir) if f.isdigit()) # python magic, Will S original version
    except:
        raise ValueError(f'No numeric folder found in {zip_name}.')

    # day_path = filepath of temp_directory concatenated with numerical_folder name
    numerical_folder_path = os.path.join(temp_dir, numerical_folder) 

    # We're gonna count how many jsons get unzipped
    json_count = 0

    # Triple unpacking jsons, write each json to the data folder
    for dirpath, dirnames, filenames in os.walk(numerical_folder_path): # os.walk() yields a 3-tuple
        for filename in filenames:
            if filename.endswith('.gz'):
                gz_path = os.path.join(dirpath, filename)
                json_filename = filename[:-3] # All characters of filename except for the last three
                output_path = os.path.join(data_dir, json_filename) # filepath = data folder 

                with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                    shutil.copyfileobj(gz_file, out_file) # copying one file to the other location
                
                json_count += 1
    
    print(f'{json_count} jsons unzipped from {zip_name}. Find them in {data_dir} folder.')