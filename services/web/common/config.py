import os

config = {
  'UPLOAD_ENDPOINT_URL': os.getenv('UPLOAD_ENDPOINT_URL'),
  'UPLOAD_S3_BUCKET': os.getenv('UPLOAD_S3_BUCKET'),
  'MEDIA_CONTENT_TYPES': ['png', 'jpg', 'jpeg', 'webp', 'gif'],
  'MAX_THREADS_PER_PAGE': 10,
  'MAX_POSTS_PER_PAGE': 100
}

def get_client_config(ipv4_addr):
  # admin config
  if ipv4_addr in os.getenv('ADMIN_IPS'):
    return {**config, **{
      'USER_ROLE': 'ADMINISTRATOR'
    }}
  # user config
  else:
    return {**config, **{
      'USER_ROLE': 'USER'
    }}
