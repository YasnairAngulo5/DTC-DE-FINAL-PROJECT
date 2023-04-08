
from web_to_gcs import ingestion_flow
from prefect.deployments import Deployment

deployment = Deployment.build_from_flow(
    flow=ingestion_flow,
    name="Ingestion Deployment",
)

if __name__ == "__main__":
    deployment.apply()