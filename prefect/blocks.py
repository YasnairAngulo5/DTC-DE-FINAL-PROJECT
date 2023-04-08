from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from pathlib import Path
import json
import os
from settings import GCS_BUCKET_NAME, GCS_CRED_RESOURCES, GCS_CRED_WB_DATA, SERVICE_ACCOUNT_FILENAME, GCS_BUCKET_RESOURCES, GCS_CREDENTIALS_BLOCK 

# This is an alternative to creating GCP blocks in the UI
# (1) insert your own GCS bucket name
# (2) insert your own service_account_file path or service_account_keys dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!


# Get the path where the credentials are saved
root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
service_account_path = os.path.join(root_directory, SERVICE_ACCOUNT_FILENAME)

with open(service_account_path) as f:
    service_account_keys = json.load(f) 


#GCP credential Blocks
cred_resources_block = GcpCredentials(
    service_account_info=service_account_keys
).save(f"{GCS_CREDENTIALS_BLOCK}",overwrite=True)

print(f"GCP credential block('{GCS_CREDENTIALS_BLOCK}') created...")


#GCP Bucket Blocks
#GCP Storage Block
bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(f"{GCS_CREDENTIALS_BLOCK}"),
    bucket=f"{GCS_BUCKET_NAME}",
).save(f"{GCS_BUCKET_NAME}", overwrite=True)

print(f"GCP bucket block('{GCS_BUCKET_NAME}') created...")

bucket_resource_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(f"{GCS_CREDENTIALS_BLOCK}"),
    bucket=f"{GCS_BUCKET_RESOURCES}",
).save(f"{GCS_BUCKET_RESOURCES}", overwrite=True)

print(f"GCP bucket block('{GCS_BUCKET_RESOURCES}') created...")
