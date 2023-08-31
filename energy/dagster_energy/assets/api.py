import requests
import json
from dagster import asset, MonthlyPartitionsDefinition, get_dagster_logger, DailyPartitionsDefinition
from datetime import datetime, timedelta, timezone, date
import calendar

logger = get_dagster_logger()
def end_of_month(date_str):
    d = datetime.strptime(date_str, '%Y-%m-%d').date()
    return date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])

@asset(description="This is a api asset",
        io_manager_key = "io_manager", 
        required_resource_keys= {"minio_resource"},
        partitions_def=DailyPartitionsDefinition(start_date="2020-06-01")
        
        )
def fetch_and_save_api_data(context):
    # 1. Determine the date range for fetching data
    partition_date = context.asset_partition_key_for_output()
    c_start_date = datetime.strptime(partition_date, '%Y-%m-%d').strftime('%Y-%m-%dT00:00:00Z')
    c_end_date = datetime.strptime(partition_date, '%Y-%m-%d').strftime('%Y-%m-%dT23:59:59Z')
    # c_end_date = end_of_month(partition_date).strftime('%Y-%m-%dT23:59:59Z')
    logger.info(f"start date {c_start_date}   end date {c_end_date}")
    
    # current_utc_date = datetime.utcnow().date()
    # start_date = current_utc_date
    # end_date = current_utc_date + timedelta(days=1)

    # 2. Set the base URL and parameters for the API request
    base_url = 'https://api.energidataservice.dk/dataset/ConsumptionDE35Hour'
    params = {
        'start': c_start_date,
        'end': c_end_date,
        'limit': '0'
    }

    # 3. Fetch data from the API using headers and parameters
    response = requests.get(base_url, params=params)
    result = response.json()

    # 4. Convert the fetched data to a string format
    data_str = json.dumps(result)

    # 5. Determine the filename and folder structure for MinIO
    folder_name = partition_date.strftime('%Y-%m-%d')
    descriptive_filename = f"energy_consumption_{partition_date}.json"
    full_path = f"{folder_name}/{descriptive_filename}"
    saved_files = []
    # 6. Save the data to MinIO
    if context.resources.minio_resource.save_file('energy-api', full_path, data_str):
        saved_files.append(full_path)
    
    return saved_files

