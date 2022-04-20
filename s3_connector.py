from io import BytesIO
import os
import boto3


"""
Simple S3 connector
"""

class S3Connector:
    def __init__(self, aws_access_key, aws_secret, region_name = "us-east-1"):
        self.session = boto3.Session(os.environ[aws_access_key], os.environ[aws_secret], region_name=region_name)
        self._s3 = self.session.resource("s3")

    def put_object_bucket(self, bucket_name, object, key):
        bucket = self._s3.Bucket(bucket_name)
        bucket.put_object(Body=object.getvalue(), Key=key)
        print(f"object saved in {bucket_name} with key {key}")