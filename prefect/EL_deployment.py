
from etl_extraction_load import extraction_load_flow, extraction_flow, load_flow
from prefect.deployments import Deployment

deployment_el = Deployment.build_from_flow(
    flow=extraction_load_flow,
    name="Extraction and load Deployment",
)

deployment_extraction = Deployment.build_from_flow(
    flow=extraction_flow,
    name="Extraction Deployment",
)

deployment_load = Deployment.build_from_flow(
    flow=load_flow,
    name="Load Deployment",
)

if __name__ == "__main__":
    deployment_el.apply()
    deployment_extraction.apply()
    deployment_load.apply()