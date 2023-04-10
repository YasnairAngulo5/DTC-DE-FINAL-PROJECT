# Configuring GCP & Terraform

[Video](https://www.youtube.com/watch?v=Hajwnmj0xfQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

### GCP
* Google Cloud Storage (GCS): Data Lake
* BigQuery: Data Warehouse

#### Initial Setup
1. Create an account with your Google email ID 
2. Setup your first [project](https://console.cloud.google.com/) using `dtc-de-project-382603` id project.
    * eg. "DTC DE Project", and in "Project ID" write  `dtc-de-project-382603`.
3. Setup [service account & authentication](https://cloud.google.com/iam/docs/service-accounts-create#iam-service-accounts-create-gcloud) for this project
   * Grant `Viewer`, `Storage Admin`, `Storage Object Admin` and `BigQuery Admin`  roles.
   * Download service-account-keys (.json) for auth and **saved it in the root of your project** with `service_account_keys` name.
4. Enable these APIs for your project:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com 
5. Download [SDK](https://cloud.google.com/sdk/docs/quickstart) for local setup
6. Set environment variable to point to your downloaded GCP keys:
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
   
   # Refresh token/session, and verify authentication
   gcloud auth application-default login
   ```


### Terraform
#### Pre-Requisites
1. Terraform client installation: https://www.terraform.io/downloads
2. Cloud Provider account: https://console.cloud.google.com/ 

#### Execution
In the terminal go to [terraform](/terraform/) folder and run:
```shell
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"
```

```shell
# Create new infra
terraform apply -var="project=<your-gcp-project-id>"
```

```shell
# Delete infra after your work, to avoid costs on any running services
terraform destroy -var="project=<your-gcp-project-id>"
```

These commands will create:
Buckets:
- `dtc_resources_bucket` with the indicators file inside. In case you want to add or update the indicators, modify the file `indicators.csv`
- `dtc_wb_data_lake` to upload the raw data

Datasets:
- bank_data
- development
- staging
- production



