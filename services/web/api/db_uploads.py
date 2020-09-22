import os
import uuid
from common.config import config
from common.dbinstance import DbInstance
from common.s3client import S3Client

def init_upload(file_name: str, file_ext: str, ipv4_addr:str, storage:str='local'):
  file_upload_info = {}

  file_uuid = uuid.uuid4()

  # local uploads
  if storage == 'local':
    file_upload_info['storage'] = 'local'
    file_upload_info['url'] = config['UPLOAD_ENDPOINT_URL']
    file_upload_info['fields'] = {
      'filename': f'{file_uuid}.{file_ext}'
    }
  # s3 uploads
  elif storage == 's3':
    file_upload_info = S3Client().instance.generate_presigned_post(
      os.getenv('MEDIA_BUCKET'),
      f'{file_uuid}.{file_ext}',
      Fields={
        'acl': 'public-read',
        'Content-Type': f'image/{file_ext}'
      },
      Conditions=[
        {'acl': 'public-read'},
        {'Content-Type': f'image/{file_ext}',
        ['content-length-range', 128, 4096000]
      ],
      ExpiresIn=60
    )
  else:
    raise Exception(f'db_uploads::init_upload error, unknown storage type {storage}')
