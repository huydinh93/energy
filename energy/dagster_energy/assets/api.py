import requests
import json
from dagster import asset
from datetime import datetime, timedelta, timezone

@asset(description="This is a api asset",
        io_manager_key = "io_manager", 
        required_resource_keys= {"minio_resource"},
        
        )
def fetch_and_save_api_data(context):
    # 1. Determine the date range for fetching data
    current_utc_date = datetime.utcnow().date()
    start_date = current_utc_date
    end_date = current_utc_date + timedelta(days=1)

    # 2. Set the base URL and parameters for the API request
    base_url = 'https://api.energidataservice.dk/dataset/ConsumptionDE35Hour'
    params = {
        'start': start_date,
        'end': end_date,
        'limit': '0'
    }

    # 3. Fetch data from the API using headers and parameters
    response = requests.get(base_url, params=params)
    result = response.json()

    # 4. Convert the fetched data to a string format
    data_str = json.dumps(result)

    # 5. Determine the filename and folder structure for MinIO
    folder_name = current_utc_date.strftime('%Y-%m-%d')
    descriptive_filename = f"energy_consumption_{current_utc_date}.json"
    full_path = f"{folder_name}/{descriptive_filename}"
    saved_files = []
    # 6. Save the data to MinIO
    if context.resources.minio_resource.save_file('energy-api', full_path, data_str):
        saved_files.append(full_path)
    
    return saved_files

