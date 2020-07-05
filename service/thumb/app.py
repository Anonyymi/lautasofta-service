import os

# init os.environ from file if not initialized
if os.getenv('DB_HOST') is None:
  import common.set_env

import io
import json
from PIL import Image
from common.dbinstance import DbInstance
from common.s3client import S3Client

def lambda_handler(evt, ctx):
  """AWS Lambda entrypoint"""
  try:
    for record in evt['Records']:
      # get object key & thumb key
      s3_key = record['s3']['object']['key']
      s3_thumbkey = 'thumb_' + s3_key.rsplit('.', 1)[0] + '.png'
      # get object data
      s3_filestr = io.BytesIO()
      S3Client().instance.download_fileobj(os.getenv('MEDIA_BUCKET'), s3_key, s3_filestr)
      s3_filestr.seek(0)
      # generate thumbnail
      image = Image.open(s3_filestr)
      image.thumbnail((256, 256,))
      s3_thumbstr = io.BytesIO()
      image.save(s3_thumbstr, format='PNG')
      s3_thumbstr.seek(0)
      # upload thumbnail data
      S3Client().instance.upload_fileobj(s3_thumbstr, os.getenv('MEDIA_BUCKET'), s3_thumbkey, ExtraArgs={
        'ACL': 'public-read',
        'ContentType': 'image/png'
      })
      # update image 'data_thumbpath' in db
      with DbInstance().get_instance().cursor() as cursor:
        cursor.execute("""
          UPDATE posts
            SET data_thumbpath = %s
          WHERE data_filepath = %s
        """, (s3_thumbkey, s3_key,))
        cursor.connection.commit()
  except Exception as err:
    print(f'{err}')
    return {
      'statusCode': 500,
      'body': json.dumps({
        'message': 'internal server error',
      })
    }
