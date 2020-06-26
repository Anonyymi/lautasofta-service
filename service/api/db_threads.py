import os
import uuid
from common.dbinstance import DbInstance
from common.s3client import S3Client

def select_threads(board_id, limit, offset):
  # prepare result
  result = {
    'status': 404,
    'data': None
  }
  # fetch rows from db
  with DbInstance().instance.cursor() as cursor:
    cursor.execute("""
      SELECT
        p.id AS id,
        p.board_id AS board_id,
        p.thread_id AS thread_id,
        p.data_message AS data_message,
        p.data_filepath AS data_filepath,
        p.datetime_created AS datetime_created,
        p.timestamp_edited AS timestamp_edited
      FROM posts AS p
      WHERE p.board_id = %s AND p.thread_id IS NULL
      ORDER BY p.timestamp_edited DESC, p.datetime_created DESC
      LIMIT %s OFFSET %s
    """, (board_id, limit, offset,))
    result['data'] = cursor.fetchall()
  # update result
  if result['data']:
    result['status'] = 200
  return result

def insert_thread(board_id, thread):
  # prepare result
  result = {
    'status': 400,
    'data': None
  }
  # generate presigned s3 url for the file
  file_upload_info = S3Client().instance.generate_presigned_post(
    os.getenv('MEDIA_BUCKET'),
    str(uuid.uuid4()) + '.' + thread['extension'],
    Fields={
      'acl': 'public-read'
    },
    Conditions=[
      ['acl', 'public-read'],
      ['content-type', thread['extension']],
      ['content-length-range', 128, 4096000]
    ],
    ExpiresIn=60
  )
  # insert row to db
  with DbInstance().instance.cursor() as cursor:
    rows = cursor.execute("""
      INSERT INTO posts (board_id, data_message, data_filepath)
      VALUES (%s, %s, %s)
    """, (board_id, thread['message'], file_upload_info['fields']['key'],))
    if rows == 1:
      cursor.connection.commit()
      result['data'] = {
        'id': cursor.lastrowid,
        'url': file_upload_info['url'],
        'fields': file_upload_info['fields']
      }
  # update result
  if result['data']:
    result['status'] = 201
  return result
