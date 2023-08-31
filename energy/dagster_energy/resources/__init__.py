from dagster_aws.s3 import S3PickleIOManager, S3Resource
from .minio_resource import MinioResource
import boto3

# minio_object = MinioResource()
# Update the configuration schema for the MinioResource
# MinioResource.config_schema = {
#     "region_name": Field(String, description="Endpoint URL for the MinIO server."),
#     "endpoint_url": Field(String, description="Endpoint URL for the MinIO server."),
#     "access_key": Field(String, description="Access key for MinIO."),
#     "secret_key": Field(String, description="Secret key for MinIO.")
# }

s3 = boto3.resource(
                            "s3",
                            region_name='us-west-1',
                            endpoint_url='http://minio-storage:9000',
                            aws_access_key_id='miniouser',
                            aws_secret_access_key='miniopassword'
                        )
if not s3.Bucket("energy-pickle-manager") in s3.buckets.all():
        s3.create_bucket(Bucket="energy-pickle-manager")


RESOURCES = {
    "local":        
                    {    
                        "minio_resource": MinioResource(region_name='us-west-1', endpoint_url ='http://minio-storage:9000', access_key = 'miniouser', secret_key = 'miniopassword'),
                        "io_manager": S3PickleIOManager(
                            s3_resource=S3Resource(region_name='us-west-1', endpoint_url ='http://minio-storage:9000', aws_access_key_id = 'miniouser', aws_secret_access_key = 'miniopassword'),
                            s3_bucket="energy-pickle-manager"
        )
                    }
}