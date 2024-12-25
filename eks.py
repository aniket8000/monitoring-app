from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "my-flask-app"}),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="084828582585.dkr.ecr.ap-south-1.amazonaws.com/my-cloud-repo",
                        ports=[client.V1ContainerPort(container_port=5000)],
                    )
                ]
            )
        )
    )
)

# Create deployment API instance
api_instance = client.AppsV1Api(api_client)

# Check if the deployment exists and update or create it
try:
    # Try to read the existing deployment
    api_instance.read_namespaced_deployment(name="my-flask-app", namespace="default")
    print("Deployment already exists. Updating the deployment.")
    # Update the deployment
    api_instance.replace_namespaced_deployment(name="my-flask-app", namespace="default", body=deployment)
except ApiException as e:
    if e.status == 404:
        # Deployment doesn't exist, create it
        print("Deployment doesn't exist. Creating new deployment.")
        api_instance.create_namespaced_deployment(namespace="default", body=deployment)
    else:
        raise e

# Define service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},  # Correct the selector here (fixed typo "my-flask-appp")
        ports=[client.V1ServicePort(port=5000)]
    )
)

# Create service API instance
api_instance_service = client.CoreV1Api(api_client)

# Check if the service exists and update or create it
try:
    # Try to read the existing service
    api_instance_service.read_namespaced_service(name="my-flask-service", namespace="default")
    print("Service already exists. Updating the service.")
    # Update the service (This is a bit tricky as there's no direct "replace" for services, so we delete and create again)
    api_instance_service.delete_namespaced_service(name="my-flask-service", namespace="default")
    api_instance_service.create_namespaced_service(namespace="default", body=service)
except ApiException as e:
    if e.status == 404:
        # Service doesn't exist, create it
        print("Service doesn't exist. Creating new service.")
        api_instance_service.create_namespaced_service(namespace="default", body=service)
    else:
        raise e
