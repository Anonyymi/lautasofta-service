import os
import botocore.client
import boto3
from common.singleton import Singleton

class S3Client(metaclass=Singleton):
  instance: botocore.client.BaseClient

  def __init__(self):
    self.session = boto3.session.Session()
    self.instance = self.session.client(
      service_name='s3',
      endpoint_url=os.getenv('S3_ENDPOINT_URL')
    )
