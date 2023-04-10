# This WF will perform:
# Extraction: From web to GCS
# Load: From GCS to BigQuery

import os
from typing import List
import pandas as pd
import datetime
import requests
import zipfile
import io
from prefect import flow, task
from pathlib import Path
from random import randint
from settings import GCS_BUCKET_NAME, GCS_BUCKET_RESOURCES, GCS_CREDENTIALS_BLOCK, PROJECT_ID
from prefect_gcp.cloud_storage import GcsBucket
from google.cloud.exceptions import NotFound
from prefect_gcp import GcpCredentials




@task(log_prints=True, )
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
def write_to_gcs(df: pd.DataFrame, year: int, month: int, indicator: str) -> str:

    indicator = indicator.replace('.', '_')
    """Uploading local  file to GCS"""
    gcs_filename = f'{year}/{month:02}/{indicator}.csv'

    gcs_bucket = GcsBucket.load(GCS_BUCKET_NAME)

    gcs_bucket.upload_from_dataframe(
        df=df, 
        to_path=gcs_filename, 
        serialization_format='csv'
    )

    return gcs_filename


@flow(log_prints=True)
def web_to_gcs(year: int, month: int, indicator: str) -> tuple[int,str]:

    try:
        dataset_url     = f'http://api.worldbank.org/v2/es/indicator/{indicator}?downloadformat=csv'
        df              = fetch(dataset_url, indicator)
        file_processed  = write_to_gcs(df, year, month, indicator)
        return len(df), file_processed
    except Exception as e:
        # handle the exception as per your requirements
        print(f"An exception occurred: {e}")
        return 0, ""

@task()
def extract_from_gcs(from_path:str, local_path: str, bucket_name:str) -> Path:
    print(f'from_path: {from_path}, local_path: {local_path}')
    gcs_bucket = GcsBucket.load(bucket_name)
    gcs_bucket.get_directory(from_path=from_path, local_path=local_path)
    return Path(f"{local_path}/{from_path}")

@task()
def write_bq(df:pd.DataFrame) -> None:
    """Write DataFrame to BigQuery"""

    gcp_credentials_block = GcpCredentials.load(GCS_CREDENTIALS_BLOCK)

    df.to_gbq(
        destination_table="bank_data.world_bank",
        project_id=PROJECT_ID,
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )
@task(log_prints=True)
def transform_data_to_schema(path: Path) -> pd.DataFrame:
    # Define the schema with data types
    dtype = {'Country Name': 'string', 
        'Country Code': 'string', 
        'Indicator Name': 'string', 
        'Indicator Code': 'string'
        }

    # read the csv file and create the dataframe
    df = pd.read_csv(path, dtype = dtype)
    
    df = df.drop(columns=['Unnamed: 66'])

    # get the index of the "Indicator Code" column
    indicator_code_index = df.columns.get_loc("Indicator Code")

    # select all columns after the "Indicator Code" column
    columns_years = df.columns[indicator_code_index+1:]

    # create a list of the columns to keep, including the "Indicator Code" column
    columns_to_keep = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'] + list(columns_years)

    # select the columns to keep
    df = df[columns_to_keep]

    # use the melt() function to convert the year columns to a single "year" column
    df = df.melt(id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'], var_name='year', value_name='value')
    df = df.rename(columns={'Country Name': 'country_name', 'Country Code': 'country_code', 'Indicator Name': 'ind_name', 'Indicator Code': 'ind_code'})

    # change data type of 'year' column to integer
    df['year'] = df['year'].astype(int)

    # Add a new column called 'created_on' as the first column
    #df.insert(0, 'created_on', pd.Timestamp('now'))

    return df 

@flow(log_prints=True)
def extraction_flow(year: int = datetime.datetime.now().year, month: int = datetime.datetime.now().month) -> None:
    
    gcs_path    = f'indicators.csv'
    path = extract_from_gcs(gcs_path, f"../resources/", GCS_BUCKET_RESOURCES)
    column_name = 'indicator code'
    df_indicators = pd.read_csv(path, 
                                names=[column_name], 
                                skiprows=1)
    indicators = df_indicators[column_name].tolist()
    print("------ Indicators Extraction Process -----")
    print(indicators)
    
    total_rows_processed = 0
    file_processed = None
    for indicator in indicators:
        rows_processed, file_processed = web_to_gcs(year, month, indicator)
        total_rows_processed += rows_processed
        print(f'File processed: {file_processed} | Rows: {total_rows_processed}')

    print(f'Extraction process finished..')
    

@flow(log_prints=True)
def load_flow(year: int = datetime.datetime.now().year, month: int = datetime.datetime.now().month) -> None:
    
    gcs_path    = f'indicators.csv'
    path = extract_from_gcs(gcs_path, f"../resources/", GCS_BUCKET_RESOURCES)
    column_name = 'indicator code'
    df_indicators = pd.read_csv(path, 
                                names=[column_name], 
                                skiprows=1)
    indicators = df_indicators[column_name].tolist()
    print("------ Indicators Load Process -----")
    print(indicators)

    for indicator in indicators:
        indicator = indicator.replace('.', '_')
        gcs_path    = f'{year}/{month:02}/{indicator}.csv'
        path = extract_from_gcs(gcs_path, f"../data/", GCS_BUCKET_NAME)
        df = transform_data_to_schema(path)
        write_bq(df)
        #final_df = final_df.append(df, ignore_index=True)
     
    print(f'Loading process finished..')


@flow(log_prints=True)
def el_test(year: int = datetime.datetime.now().year, month: int = datetime.datetime.now().month):
    indicator = 'NY.GDP.MKTP.KD.ZG'
    

    #Extraction
    rows_processed, file_processed = web_to_gcs(year, month, indicator)
    print(f'File processed: {file_processed} | Rows: {rows_processed}')

    print(f'Extraction process finished..')

    #Load
    indicator = indicator.replace('.', '_')
    gcs_path    = f'{year}/{month:02}/{indicator}.csv'
    path = extract_from_gcs(gcs_path, f"../data/", GCS_BUCKET_NAME)
    print('BEFORE TRANSFORM DATA')
    df = transform_data_to_schema(path)
    write_bq(df)
    print(f'Loading process finished..')
    

    



@flow(log_prints=True)
def extraction_load_flow(year: int = datetime.datetime.now().year, month: int = datetime.datetime.now().month):

    
    
    # Extraction process
    extraction_flow(year, month)

    # Load process
    load_flow(year, month)

    '''    
    # Test
    el_test(1990, month)
    
    rows_processed = 0
    file_processed = None
    for indicator in indicators:
        rows_processed, file_processed = web_to_gcs(month, indicator)
        print(f'File processed: {file_processed} | Rows: {rows_processed}')
    '''

if __name__ == '__main__':
    year            = datetime.datetime.now().year
    month           = datetime.datetime.now().month
    extraction_flow(year, month)

