import os

config = {
  'MEDIA_BUCKET_URL': os.getenv('S3_ENDPOINT_URL') + '/' + os.getenv('MEDIA_BUCKET'),
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
