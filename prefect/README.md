# Configuring Prefect Cloud
For this project I decided to use prefect cloud.

1. Login into [prefect cloud](https://app.prefect.cloud/auth/login) and create a workspace for this project or reuse one.
2. In your terminal run:
```
    prefect cloud login
```
3. Once you are logged, in your terminal go to the [prefect](/prefect) folder and execute the files [blocks.py](/prefect/blocks.py)(to create the prefect blocks) and [ingest_deployment.py](/prefect/ingest_deployment.py) to deploy the wf that will run the ingestion of data process:
```
    python3 blocks.py
```
```
    python3 ingest_deployment.py
```
*Note:* In [settings.py](/prefect/settings.py) file you can configure the name of the blocks you need to create.
4. To deploy the ingestion workglow


## Process
### Parameters



