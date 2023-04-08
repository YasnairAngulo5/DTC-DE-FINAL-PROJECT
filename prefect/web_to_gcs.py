import os
from typing import List
import pandas as pd
import datetime
import requests
import zipfile
import io
from prefect import flow, task
from google.cloud import storage
from random import randint
from settings import GCS_BUCKET_NAME, GCS_BUCKET_RESOURCES
from prefect_gcp.cloud_storage import GcsBucket
from google.cloud.exceptions import NotFound
from prefect_gcp import GcpCredentials




@task(log_prints=True, retries=3)
def fetch(url: str, indicator: str) -> pd.DataFrame:
    """Read worldbank data from web into pandas DataFrame"""
    r = requests.get(url)
    filename = f'API_{indicator}' #the prefix of the file we are interested in.

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        for name in z.namelist():
            if name.startswith(filename):
                with z.open(name) as f:
                    contenido = f.read().decode('utf-8')

    df = pd.read_csv(io.StringIO(contenido), skiprows=4)
    return df


@task(log_prints=True)
def write_to_gcs(df: pd.DataFrame, month: int, indicator: str) -> None:

    """Uploading local  file to GCS"""
    current_year = datetime.datetime.now().year
    gcs_filename = f'{current_year}-{month:02}/{indicator}.csv'

    gcs_bucket = GcsBucket.load(GCS_BUCKET_NAME)
    gcs_bucket.upload_from_dataframe(
        df=df, 
        to_path=gcs_filename, 
        serialization_format='csv'
    )

    '''
    # Get the path where the credentials are saved
    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    service_account_path = os.path.join(root_directory, SERVICE_ACCOUNT_FILENAME)

    client = storage.Client.from_service_account_json(json_credentials_path=service_account_path)

    # The bucket on GCS in which to write the CSV file
    bucket = client.bucket(GCS_BUCKET_NAME)
    # The name assigned to the CSV file on GCS
    blob = bucket.blob(gcs_filename)
    blob.upload_from_string(df.to_csv(), 'text/csv')
    '''

@task(log_prints=True)
def get_indicators() -> List:
    '''
    # Load the GCP credentials
    gcp_credentials_block = GcpCredentials.load("dtc-wb-creds")

    # Create a credentials object from the GCP credentials block
    creds = gcp_credentials_block.credentials
    # Use the credentials to create a client for Google Cloud Storage
    client = storage.Client(project=gcp_credentials_block.project_id, credentials=creds)
    # Use the client to get the CSV file from GCS
    bucket = client.get_bucket(GCS_BUCKET_RESOURCES)
    blob = bucket.blob('indicators.csv')
    data = blob.download_as_string()

    # Use pandas to read the CSV data
    df = pd.read_csv(data)
    print(df)

    '''
    try:
        #get indicators list
        column_name = 'indicator code'
        df_indicators = pd.read_csv(f'gs://{GCS_BUCKET_RESOURCES}/indicators.csv', names=[column_name], skiprows=1)
        indicators = df_indicators[column_name].tolist()
        return indicators 
    except NotFound:
        print(f"File not found in GCS bucket: gs://{GCS_BUCKET_RESOURCES}/indicators.csv")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    
    

@flow()
def web_to_gcs(month: int, indicator: str) -> int:
    
    dataset_url    = f'http://api.worldbank.org/v2/es/indicator/{indicator}?downloadformat=csv'
    df              = fetch(dataset_url, indicator)
    write_to_gcs(df, month, indicator)
    return len(df)

@flow(log_prints=True)
def ingestion_flow(month: int = 4):

    total_rows_processed = 0
    # Getting indicators
    indicators = get_indicators()
    print("------ Indicators -----")
    print(indicators)

    for indicator in indicators:
        rows_processed = web_to_gcs(month, indicator)
        total_rows_processed= total_rows_processed + rows_processed

    print(f"Total number of rows processed: {total_rows_processed} ")
    

if __name__ == '__main__':
    month           = datetime.datetime.now().month
    ingestion_flow(month)

