import boto3

ecr_client = boto3.client("ecr")

repository_name = "my-cloud-native-repoo"
response = ecr_client.create_repository(repositoryName=repository_name)

repository_uri = response['respository']['repositoryUri']
print(repository_uri)
