from dagster import ConfigurableResource, Field, String
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


class MinioResource(ConfigurableResource):
    # Configuration schema for the resource
    endpoint_url: str
    access_key: str
    secret_key: str
    region_name: str

    def get_client(self):
        """Retrieve the MinIO client."""
        return boto3.resource(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name
        )

    def save_file(self,bucket_name, filename, data):
        """Save data to a file in the specified MinIO bucket."""
        client = self.get_client()
        
        # Ensure the bucket exists
        self._ensure_bucket_exists(client, bucket_name)
        
        try:
            client.Object(bucket_name, filename).put(Body=data)
        except NoCredentialsError:
            raise Exception("Credentials not available")

    def _ensure_bucket_exists(self, client, bucket_name):
        """Ensure the specified bucket exists in MinIO. If not, create it."""
        if not client.Bucket(bucket_name) in client.buckets.all():
            client.create_bucket(Bucket=bucket_name)