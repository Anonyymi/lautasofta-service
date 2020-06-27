import os

config = {
  'MEDIA_BUCKET_URL': os.getenv('S3_ENDPOINT_URL') + '/' + os.getenv('MEDIA_BUCKET'),
  'MEDIA_CONTENT_TYPES': ['png', 'jpg', 'jpeg', 'gif']
}
