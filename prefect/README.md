# Configuring Prefect Cloud
For this project I decided to use prefect cloud to perform extraction and loas process

1. Login into [prefect cloud](https://app.prefect.cloud/auth/login) and create a workspace for this project or reuse one.
2. In your terminal run:
```
    prefect cloud login
```
3. Once you are logged, in your terminal go to the [prefect](/prefect) folder and execute the files [blocks.py](/prefect/blocks.py)(to create the prefect blocks) and [EL_deployment.py](/prefect/EL_deployment.py) to deploy the wf that will run the extraction and loading of data process:
```
    python3 blocks.py
```
```
    python3 EL_deployment.py
```

*Note:* In [settings.py](/prefect/settings.py) file you can configure the name of the blocks you need to create.

The [EL_deployment.py](/prefect/EL_deployment.py) will create the following flows:
- `extraction_load_flow` to execute extraction and loading  process
- `extraction_flow`to execute extraction process.
- `load_flow`to execute load process.
  
## Process

### Parameters



