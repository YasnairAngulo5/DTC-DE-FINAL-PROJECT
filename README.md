# World Bank KPI's
## Overview


## Problem Statment

## Data Sources:

## Tools & Tech Stack Used: (REVISAR)
1. Infrastructure as Code(IaC) --> [Terraform](https://www.terraform.io)
2. Cloud Platform --> [Google Cloud](https://cloud.google.com)
3. Data Lake --> [Google Cloud Storage](https://cloud.google.com/storage/)
4. Data Warehouse --> [Google BigQuery](https://cloud.google.com/bigquery)
5. Data Transformation:
  a.Pre Load --> [Python Pandas Library](https://pandas.pydata.org) and [Python Pyarrow Library](https://arrow.apache.org/docs/python/index.html)
  b.Post Load Batch Processing --> [Apache Spark](https://spark.apache.org) and [Google DataProc](https://cloud.google.com/dataproc)
6. Workflow Orchestration --> [Airflow](https://airflow.apache.org)
7. Containerization --> [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/)
8. Data Vizualization Tool --> [Google Data Studio](https://datastudio.google.com/)

## Data Pipeline Architecture:

## Step-by-Step-Guide
1. Clone the repository
2. Create and activate a virtual enviroment.
   ```bash
    python3 -m venv .venv 
    source .venv/bin/activate
   ```
3. Install the packages required in the [requirements.txt](/requirements.txt) file.
   ```bash
      pip3 install -r requirements.txt  
   ```
4. Provisión Cloud Insfrastructure
   Go to [Local Setup for Terraform and GCP](/terraform/README.md) and configure GCP & Terraform.
   **Important:** do not forget to download service-account-keys (.json) for auth and saved it in the *root* of your project with the `service_account_keys.json` file name.
5. Configure and execute [prefect](/prefect/README.md) to move the files from the hard disk to gcs.
   


