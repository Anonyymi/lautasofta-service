import os
import uuid
from common.dbinstance import DbInstance
from common.s3client import S3Client

def select_posts(board_id, thread_id, limit, offset):
  # prepare result
  result = {
    'status': 404,
    'data': None
  }
  # fetch rows from db
  with DbInstance().get_instance().cursor() as cursor:
    cursor.execute("""
      SELECT
        p.id AS id,
        p.board_id AS board_id,
        p.thread_id AS thread_id,
        p.data_message AS data_message,
        p.data_filepath AS data_filepath,
        DATE_FORMAT(p.datetime_created, '%%m/%%d/%%y(%%a)%%T') AS datetime_created,
        DATE_FORMAT(p.timestamp_edited, '%%m/%%d/%%y(%%a)%%T') AS timestamp_edited
      FROM posts AS p
      WHERE p.board_id = %s AND p.thread_id = %s OR p.id = %s
      ORDER BY p.datetime_created ASC
      LIMIT %s OFFSET %s
    """, (board_id, thread_id, thread_id, limit, offset,))
    result['data'] = cursor.fetchall()
  # update result
  if result['data']:
    result['status'] = 200
  return result

def insert_post(board_id, thread_id, post, ipv4_addr):
  # prepare result
  result = {
    'status': 400,
    'data': None
  }
  # if requested, generate presigned s3 POST url for the file
  file_upload_info = {
    'url': None,
    'fields': {
      'key': None
    },
  }
  if post['extension'] is not None:
    file_upload_info = S3Client().instance.generate_presigned_post(
      os.getenv('MEDIA_BUCKET'),
      str(uuid.uuid4()) + '.' + post['extension'],
      Fields={
        'acl': 'public-read'
      },
      Conditions=[
        ['acl', 'public-read'],
        ['content-type', post['extension']],
        ['content-length-range', 128, 4096000]
      ],
      ExpiresIn=60
    )
  # insert row to db
  with DbInstance().get_instance().cursor() as cursor:
    # insert/update ipv4_addr row
    rows_anon = cursor.execute("""
      INSERT INTO anons (ipv4_addr) VALUES (INET_ATON(%s))
      ON DUPLICATE KEY UPDATE timestamp_posted=CURRENT_TIMESTAMP
    """, (ipv4_addr,))
    # insert post
    rows_post = cursor.execute("""
      INSERT INTO posts (board_id, thread_id, data_message, data_filepath, ipv4_addr)
      VALUES (%s, %s, %s, %s, INET_ATON(%s))
    """, (board_id, thread_id, post['message'], file_upload_info['fields']['key'], ipv4_addr,))
    id_inserted = cursor.lastrowid
    # update thread
    rows_thread = cursor.execute("""
      UPDATE posts
      SET timestamp_bumped = CURRENT_TIMESTAMP
      WHERE board_id = %s AND id = %s;
    """, (board_id, thread_id,))
    # commit if ok
    if rows_anon >= 1 and rows_post == 1 and rows_thread == 1:
      cursor.connection.commit()
      result['data'] = {
        'id': id_inserted,
        'url': file_upload_info['url'],
        'fields': file_upload_info['fields']
      }
  # update result
  if result['data']:
    result['status'] = 201
  return result
